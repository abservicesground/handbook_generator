import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-2024-05-13')
    
    SUPABASE_URL = os.getenv('SUPABASE_URL', '')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')
    
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')
    EMBEDDING_DIM = int(os.getenv('EMBEDDING_DIM', '1536'))
    
    MAX_CHUNK_SIZE = int(os.getenv('MAX_CHUNK_SIZE', '1000'))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '200'))
    MAX_HANDBOOK_LENGTH = int(os.getenv('MAX_HANDBOOK_LENGTH', '20000'))
    
    UPLOAD_FOLDER = 'uploads'
    CACHE_FOLDER = 'cache'
    
    @classmethod
    def validate(cls):
        missing = []
        if not cls.OPENAI_API_KEY:
            missing.append('OPENAI_API_KEY')
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True
    
    @classmethod
    def create_folders(cls):
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(cls.CACHE_FOLDER, exist_ok=True)
