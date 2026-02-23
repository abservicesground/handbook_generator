import gradio as gr
import os
from pathlib import Path
from config import Config
from pdf_processor import PDFProcessor
from openai_handler import OpenAIHandler
from rag_manager import RAGManager
from handbook_generator import HandbookGenerator
import traceback

Config.create_folders()

pdf_processor = PDFProcessor()
openai_handler = None
rag_manager = None
handbook_gen = None

conversation_history = []
uploaded_files = []

def initialize_services():
    global openai_handler, rag_manager, handbook_gen
    
    try:
        Config.validate()
        
        openai_handler = OpenAIHandler()
        rag_manager = RAGManager(working_dir=Config.CACHE_FOLDER)
        handbook_gen = HandbookGenerator(openai_handler, rag_manager)
        
        return "✅ Services initialized successfully!"
    except Exception as e:
        return f"❌ Initialization failed: {str(e)}\n\nPlease check your .env file and ensure all API keys are set."

def process_pdf_upload(file):
    global uploaded_files
    
    if file is None:
        return "❌ No file uploaded", ""
    
    try:
        file_path = file.name
        file_name = Path(file_path).name
        
        status_msg = f"📄 Processing: {file_name}...\n"
        
        result = pdf_processor.process_pdf(file_path)
        
        status_msg += f"✅ Extracted {result['total_words']} words from {result['total_chunks']} chunks\n"
        status_msg += f"📥 Adding to knowledge base...\n"
        
        rag_manager.add_document(result['full_text'], metadata={'filename': file_name})
        
        uploaded_files.append(file_name)
        
        status_msg += f"✅ Successfully processed: {file_name}\n"
        status_msg += f"📚 Total documents in system: {rag_manager.get_document_count()}"
        
        files_list = "\n".join([f"• {f}" for f in uploaded_files])
        
        return status_msg, files_list
        
    except Exception as e:
        error_msg = f"❌ Error processing PDF: {str(e)}\n\n{traceback.format_exc()}"
        return error_msg, ""

def chat(message, history):
    """
    Chat function using Gradio 6.x message format.
    History is a list of message dicts with 'role' and 'content' keys.
    """
    global conversation_history
    
    print(f"📨 Received message: {message[:50]}...")
    
    if not openai_handler or not rag_manager:
        response = "❌ Please initialize services first by entering your API keys."
        print(f"⚠️ Services not initialized")
        return history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": response}
        ]
    
    if not message or not message.strip():
        print("⚠️ Empty message received")
        return history
    
    try:
        if rag_manager.get_document_count() == 0:
            response = "⚠️ No documents uploaded yet. Please upload PDF documents first to enable contextual responses."
            print(f"⚠️ No documents in system")
            return history + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": response}
            ]
        
        print(f"📚 Documents available: {rag_manager.get_document_count()} chunks")
        
        handbook_topic = handbook_gen.detect_handbook_request(message)
        
        if handbook_topic:
            print(f"📖 Handbook request detected for: {handbook_topic}")
            response = f"📖 Detected handbook request for: **{handbook_topic}**\n\n"
            response += "🔄 Starting handbook generation... This will take several minutes.\n\n"
            response += "⏳ Generating outline and writing sections...\n"
            
            result = handbook_gen.generate_handbook(
                topic=handbook_topic,
                target_length=20000
            )
            
            if result['success']:
                response = f"✅ **Handbook Generated Successfully!**\n\n"
                response += f"📊 **Statistics:**\n"
                response += f"- Word Count: {result['word_count']:,} words\n"
                response += f"- Sections: {result['sections']}\n\n"
                response += f"---\n\n{result['content']}"
            else:
                response = f"❌ Handbook generation failed: {result.get('error', 'Unknown error')}"
            
            return history + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": response}
            ]
        
        else:
            print(f"💬 Q&A mode - retrieving context...")
            context = rag_manager.get_context_for_query(message)
            print(f"📄 Retrieved context length: {len(context)} chars")
            
            print(f"🤖 Calling OpenAI API...")
            response = openai_handler.generate_with_context(
                query=message,
                context=context,
                max_tokens=1024,
                temperature=0.7
            )
            print(f"✅ Got response: {response[:50]}...")
            
            conversation_history.append({
                'user': message,
                'assistant': response
            })
            
            # Gradio 6.x format
            return history + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": response}
            ]
    
    except Exception as e:
        error_response = f"❌ Error: {str(e)}\n\n{traceback.format_exc()}"
        print(f"❌ Error in chat: {e}")
        print(traceback.format_exc())
        return history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": error_response}
        ]

def clear_chat():
    global conversation_history
    conversation_history = []
    return []

def clear_documents():
    global uploaded_files
    
    try:
        rag_manager.clear()
        uploaded_files = []
        return "✅ All documents cleared from the system.", ""
    except Exception as e:
        return f"❌ Error clearing documents: {str(e)}", ""

def create_interface():
    app = gr.Blocks(title="AI Handbook Generator")
    
    with app:
        gr.Markdown("""
        # 📚 AI Handbook Generator
        
        Upload PDFs, ask questions, and generate comprehensive 20,000-word handbooks!
        
        ## 🚀 Getting Started:
        1. **Setup**: Create a `.env` file with your OpenAI API key (see `env_template.txt`)
        2. **Upload**: Upload one or more PDF documents
        3. **Chat**: Ask questions about your documents
        4. **Generate**: Request a handbook (e.g., "Create a handbook on Machine Learning")
        
        **Uses OpenAI GPT-4o** (same as LongWriter reference implementation)
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📤 Upload Documents")
                
                pdf_upload = gr.File(
                    label="Upload PDF",
                    file_types=[".pdf"],
                    type="filepath"
                )
                
                upload_status = gr.Textbox(
                    label="Upload Status",
                    lines=5,
                    interactive=False
                )
                
                uploaded_files_display = gr.Textbox(
                    label="Uploaded Files",
                    lines=5,
                    interactive=False,
                    placeholder="No files uploaded yet"
                )
                
                clear_docs_btn = gr.Button("🗑️ Clear All Documents", variant="secondary")
            
            with gr.Column(scale=2):
                gr.Markdown("### 💬 Chat Interface")
                
                chatbot = gr.Chatbot(
                    height=500,
                    show_label=False
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Ask a question or request a handbook...",
                        show_label=False,
                        scale=4
                    )
                    submit_btn = gr.Button("Send", variant="primary", scale=1)
                
                clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")
        
        gr.Markdown("""
        ---
        ### 💡 Tips:
        - **Q&A Mode**: Ask specific questions about your uploaded documents
        - **Handbook Mode**: Use phrases like "Create a handbook on...", "Generate a guide about...", etc.
        - **Target Length**: Handbooks aim for 20,000+ words with structured sections
        
        ### 📝 Example Prompts:
        - "What are the main findings in the uploaded research paper?"
        - "Create a comprehensive handbook on Retrieval-Augmented Generation"
        - "Generate a guide about the methodologies discussed in the documents"
        """)
        
        # Event handlers
        pdf_upload.change(
            process_pdf_upload,
            inputs=[pdf_upload],
            outputs=[upload_status, uploaded_files_display]
        )
        
        # Chat event handlers - clear message after sending
        msg.submit(
            chat, 
            inputs=[msg, chatbot], 
            outputs=[chatbot]
        ).then(
            lambda: "", 
            None, 
            msg
        )
        
        submit_btn.click(
            chat, 
            inputs=[msg, chatbot], 
            outputs=[chatbot]
        ).then(
            lambda: "", 
            None, 
            msg
        )
        
        clear_btn.click(clear_chat, outputs=[chatbot])
        clear_docs_btn.click(clear_documents, outputs=[upload_status, uploaded_files_display])
    
    return app

if __name__ == "__main__":
    print("="*60)
    print("AI Handbook Generator - Starting...")
    print("="*60)
    
    init_status = initialize_services()
    print(init_status)
    
    if "successfully" in init_status.lower():
        print("\n🌐 Launching web interface...")
        app = create_interface()
        app.queue()  # Enable queue for handling requests
        app.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False
        )
    else:
        print("\n❌ Cannot start application. Please configure your .env file.")
        print("See env_template.txt for required variables.")
