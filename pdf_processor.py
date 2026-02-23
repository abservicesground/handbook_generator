import PyPDF2
import pdfplumber
from typing import List, Dict
import re
from config import Config

class PDFProcessor:
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or Config.MAX_CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or Config.CHUNK_OVERLAP
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        text = ""
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
        except Exception as e:
            print(f"pdfplumber failed: {e}. Trying PyPDF2...")
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n\n"
            except Exception as e2:
                raise Exception(f"Both PDF extraction methods failed: {e2}")
        
        return self._clean_text(text)
    
    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\S\n]+', ' ', text)
        text = text.strip()
        return text
    
    def chunk_text(self, text: str) -> List[Dict[str, any]]:
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            chunks.append({
                'text': chunk_text,
                'start_index': i,
                'end_index': i + len(chunk_words),
                'word_count': len(chunk_words)
            })
            
            if i + self.chunk_size >= len(words):
                break
        
        return chunks
    
    def process_pdf(self, pdf_path: str) -> Dict[str, any]:
        text = self.extract_text_from_pdf(pdf_path)
        chunks = self.chunk_text(text)
        
        return {
            'full_text': text,
            'chunks': chunks,
            'total_chunks': len(chunks),
            'total_words': len(text.split()),
            'source_file': pdf_path
        }
    
    def extract_metadata(self, pdf_path: str) -> Dict[str, any]:
        metadata = {}
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                info = pdf_reader.metadata
                
                if info:
                    metadata = {
                        'title': info.get('/Title', ''),
                        'author': info.get('/Author', ''),
                        'subject': info.get('/Subject', ''),
                        'creator': info.get('/Creator', ''),
                        'producer': info.get('/Producer', ''),
                        'creation_date': info.get('/CreationDate', ''),
                        'modification_date': info.get('/ModDate', ''),
                    }
                
                metadata['num_pages'] = len(pdf_reader.pages)
        except Exception as e:
            print(f"Error extracting metadata: {e}")
        
        return metadata
