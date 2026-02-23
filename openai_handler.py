import requests
import time
from typing import List, Dict, Optional
from config import Config

class OpenAIHandler:
    """
    OpenAI API handler for generating responses.
    Based on the LongWriter reference implementation.
    """
    
    def __init__(self, api_key: str = None, api_base: str = None, model: str = None):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.api_base = api_base or Config.OPENAI_API_BASE
        self.model = model or Config.OPENAI_MODEL
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")
    
    def generate_response(
        self, 
        prompt: str, 
        max_tokens: int = 2048,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
        stop: Optional[List[str]] = None
    ) -> str:
        """
        Generate response using OpenAI API.
        Based on LongWriter's get_response_gpt4 function.
        """
        tries = 0
        max_tries = 10
        
        while tries < max_tries:
            tries += 1
            try:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
                
                messages = []
                if system_prompt:
                    messages.append({'role': 'system', 'content': system_prompt})
                messages.append({'role': 'user', 'content': prompt})
                
                payload = {
                    'model': self.model,
                    'messages': messages,
                    'temperature': temperature,
                    'max_tokens': max_tokens,
                }
                
                if stop:
                    payload['stop'] = stop
                
                response = requests.post(
                    f'{self.api_base}/chat/completions',
                    json=payload,
                    headers=headers,
                    timeout=600
                )
                
                if response.status_code != 200:
                    raise Exception(f"API Error: {response.status_code} - {response.text}")
                
                result = response.json()
                return result['choices'][0]['message']['content']
                
            except KeyboardInterrupt:
                raise
            except Exception as e:
                if "maximum context length" in str(e):
                    raise e
                elif "triggering" in str(e):
                    return 'Trigger OpenAI\'s content management policy'
                print(f'Error Occurs: "{str(e)}"        Retry ...')
                if tries < max_tries:
                    time.sleep(2)
                else:
                    print("Max tries. Failed.")
                    return "Max tries. Failed."
        
        return ""
    
    def generate_with_context(
        self,
        query: str,
        context: str,
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> str:
        """Generate response with context for Q&A."""
        system_prompt = """You are a helpful AI assistant. Use the provided context to answer questions accurately and comprehensively.
If the context doesn't contain relevant information, say so clearly."""
        
        prompt = f"""Context:
{context}

Question: {query}

Answer:"""
        
        return self.generate_response(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            system_prompt=system_prompt
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> str:
        """Chat with conversation history."""
        tries = 0
        max_tries = 10
        
        while tries < max_tries:
            tries += 1
            try:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    'model': self.model,
                    'messages': messages,
                    'temperature': temperature,
                    'max_tokens': max_tokens,
                }
                
                response = requests.post(
                    f'{self.api_base}/chat/completions',
                    json=payload,
                    headers=headers,
                    timeout=600
                )
                
                if response.status_code != 200:
                    raise Exception(f"API Error: {response.status_code} - {response.text}")
                
                result = response.json()
                return result['choices'][0]['message']['content']
                
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f'Error on attempt {tries}/{max_tries}: {str(e)}')
                if tries < max_tries:
                    time.sleep(2)
                else:
                    raise Exception(f"Failed after {max_tries} attempts: {str(e)}")
        
        return ""
