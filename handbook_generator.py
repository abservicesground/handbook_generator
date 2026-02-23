from typing import List, Dict, Optional
from openai_handler import OpenAIHandler
from rag_manager import RAGManager
import re
from tqdm import tqdm

class HandbookGenerator:
    def __init__(self, openai_handler: OpenAIHandler, rag_manager: RAGManager):
        self.openai = openai_handler
        self.rag = rag_manager
        self.plan_template = self._load_plan_template()
        self.write_template = self._load_write_template()
    
    def _load_plan_template(self) -> str:
        return """You are an expert technical writer tasked with creating a comprehensive handbook outline.

Topic: {topic}

Context from documents:
{context}

Create a detailed outline for a {target_length}-word handbook on this topic. Your outline should:
1. Include a clear table of contents structure
2. Have main sections and subsections
3. Be comprehensive and cover all important aspects
4. Each section should be substantial enough to meet the target word count
5. Format as a numbered list with section titles

Generate ONLY the outline with section titles, one per line. Example format:
1. Introduction to [Topic]
2. Fundamental Concepts
2.1. Core Principle 1
2.2. Core Principle 2
3. Advanced Topics
...

Outline:"""
    
    def _load_write_template(self) -> str:
        return """You are writing a comprehensive handbook section by section.

Topic: {topic}

Full Outline:
{plan}

Context from documents:
{context}

Previous content written:
{previous_text}

Current section to write: {current_step}

Instructions:
- Write a detailed, comprehensive section for "{current_step}"
- Target approximately {section_length} words for this section
- Use information from the provided context
- Maintain professional, clear writing
- Include examples, explanations, and details
- Ensure continuity with previous sections
- Do NOT repeat information from previous sections
- Write in complete paragraphs with proper formatting

Write the section now:"""
    
    def generate_plan(self, topic: str, context: str, target_length: int = 20000) -> List[str]:
        print("Generating handbook outline...")
        
        prompt = self.plan_template.format(
            topic=topic,
            context=context[:8000],
            target_length=target_length
        )
        
        plan_text = self.openai.generate_response(
            prompt=prompt,
            max_tokens=2048,
            temperature=0.7
        )
        
        steps = [line.strip() for line in plan_text.split('\n') if line.strip() and re.match(r'^\d', line.strip())]
        
        print(f"Generated outline with {len(steps)} sections")
        return steps
    
    def generate_section(
        self, 
        topic: str,
        plan: List[str],
        current_step: str,
        context: str,
        previous_text: str,
        section_length: int = 1000
    ) -> str:
        prompt = self.write_template.format(
            topic=topic,
            plan='\n'.join(plan),
            context=context[:6000],
            previous_text=previous_text[-3000:] if previous_text else "None - this is the first section",
            current_step=current_step,
            section_length=section_length
        )
        
        section = self.openai.generate_response(
            prompt=prompt,
            max_tokens=2048,
            temperature=0.7
        )
        
        return section
    
    def generate_handbook(
        self, 
        topic: str,
        target_length: int = 20000,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, any]:
        print(f"\n{'='*60}")
        print(f"Starting handbook generation: {topic}")
        print(f"Target length: {target_length} words")
        print(f"{'='*60}\n")
        
        context = self.rag.get_all_documents_text()
        
        if not context:
            return {
                'success': False,
                'error': 'No documents available. Please upload PDFs first.',
                'content': '',
                'word_count': 0
            }
        
        plan = self.generate_plan(topic, context, target_length)
        
        if not plan:
            return {
                'success': False,
                'error': 'Failed to generate outline',
                'content': '',
                'word_count': 0
            }
        
        num_sections = len(plan)
        section_length = max(800, target_length // num_sections)
        
        print(f"\nOutline created with {num_sections} sections")
        print(f"Target per section: ~{section_length} words\n")
        
        full_text = f"# {topic}\n\n"
        full_text += "## Table of Contents\n\n"
        for step in plan:
            full_text += f"- {step}\n"
        full_text += "\n---\n\n"
        
        sections_content = []
        
        for idx, step in enumerate(tqdm(plan, desc="Writing sections")):
            print(f"\nWriting section {idx+1}/{num_sections}: {step}")
            
            if progress_callback:
                progress_callback(idx + 1, num_sections, step)
            
            try:
                relevant_context = self.rag.get_context_for_query(step)
                
                section = self.generate_section(
                    topic=topic,
                    plan=plan,
                    current_step=step,
                    context=relevant_context,
                    previous_text=full_text,
                    section_length=section_length
                )
                
                section_header = f"## {step}\n\n"
                section_with_header = section_header + section + "\n\n"
                
                sections_content.append(section_with_header)
                full_text += section_with_header
                
                current_word_count = len(full_text.split())
                print(f"Section complete. Current total: {current_word_count} words")
                
            except Exception as e:
                print(f"Error writing section {step}: {e}")
                continue
        
        final_word_count = len(full_text.split())
        
        print(f"\n{'='*60}")
        print(f"Handbook generation complete!")
        print(f"Final word count: {final_word_count}")
        print(f"Target was: {target_length}")
        print(f"{'='*60}\n")
        
        return {
            'success': True,
            'content': full_text,
            'word_count': final_word_count,
            'sections': len(sections_content),
            'outline': plan
        }
    
    def detect_handbook_request(self, message: str) -> Optional[str]:
        handbook_keywords = [
            'handbook', 'manual', 'guide', 'documentation',
            'comprehensive', 'detailed document', 'create a book',
            'write a guide', 'generate documentation'
        ]
        
        message_lower = message.lower()
        
        for keyword in handbook_keywords:
            if keyword in message_lower:
                return self._extract_topic(message)
        
        return None
    
    def _extract_topic(self, message: str) -> str:
        patterns = [
            r'handbook (?:on|about|for) (.+)',
            r'guide (?:on|about|for|to) (.+)',
            r'manual (?:on|about|for) (.+)',
            r'documentation (?:on|about|for) (.+)',
            r'create (?:a|an) .+ (?:on|about) (.+)',
            r'write (?:a|an) .+ (?:on|about) (.+)',
        ]
        
        message_lower = message.lower()
        
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                topic = match.group(1).strip()
                topic = re.sub(r'[.!?]$', '', topic)
                return topic
        
        return "the uploaded documents"
