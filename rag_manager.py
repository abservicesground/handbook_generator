import os
from typing import List, Dict, Optional
from config import Config
import json

class RAGManager:
    """
    Simplified RAG Manager without LightRAG dependency.
    Stores documents and performs basic context retrieval.
    """
    
    def __init__(self, working_dir: str = "./cache"):
        self.working_dir = working_dir
        os.makedirs(working_dir, exist_ok=True)
        
        self.documents = []
        self.cache_file = os.path.join(working_dir, "documents.json")
        
        # Load existing documents if any
        self._load_documents()
    
    def _load_documents(self):
        """Load documents from cache file."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
                print(f"Loaded {len(self.documents)} documents from cache")
            except Exception as e:
                print(f"Error loading documents: {e}")
                self.documents = []
    
    def _save_documents(self):
        """Save documents to cache file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving documents: {e}")
    
    def add_document(self, text: str, metadata: Optional[Dict] = None):
        """Add a document to the RAG system."""
        try:
            # Split text into chunks for better retrieval
            chunks = self._chunk_text(text)
            
            for i, chunk in enumerate(chunks):
                self.documents.append({
                    'text': chunk,
                    'metadata': metadata or {},
                    'chunk_id': i,
                    'length': len(chunk)
                })
            
            self._save_documents()
            print(f"Document added successfully. Total chunks: {len(self.documents)}")
        except Exception as e:
            print(f"Error adding document: {e}")
            raise
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks."""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
            
            if i + chunk_size >= len(words):
                break
        
        return chunks if chunks else [text]
    
    def query(self, query: str, top_k: int = 3) -> str:
        """
        Query documents and return relevant context.
        Uses simple keyword matching.
        """
        try:
            if not self.documents:
                return ""
            
            # Simple keyword-based retrieval
            query_words = set(query.lower().split())
            
            # Score each document chunk
            scored_docs = []
            for doc in self.documents:
                doc_words = set(doc['text'].lower().split())
                # Calculate overlap score
                overlap = len(query_words & doc_words)
                if overlap > 0:
                    scored_docs.append((overlap, doc['text']))
            
            # Sort by score and take top_k
            scored_docs.sort(reverse=True, key=lambda x: x[0])
            top_docs = [doc[1] for doc in scored_docs[:top_k]]
            
            # Combine top documents
            context = "\n\n".join(top_docs)
            return context
            
        except Exception as e:
            print(f"Error in query: {e}")
            return ""
    
    def get_context_for_query(self, query: str, max_length: int = 4000) -> str:
        """Get context for a query with length limit."""
        context = self.query(query, top_k=3)
        
        if len(context) > max_length:
            context = context[:max_length] + "..."
        
        return context
    
    def clear(self):
        """Clear all documents."""
        self.documents = []
        self._save_documents()
        print("Document cache cleared")
    
    def get_document_count(self) -> int:
        """Get total number of document chunks."""
        return len(self.documents)
    
    def get_all_documents_text(self) -> str:
        """Get all document text combined."""
        if not self.documents:
            return ""
        
        # Get unique text (avoid duplicates from overlapping chunks)
        unique_texts = []
        seen = set()
        
        for doc in self.documents:
            text = doc['text']
            if text not in seen:
                unique_texts.append(text)
                seen.add(text)
        
        return "\n\n".join(unique_texts)
