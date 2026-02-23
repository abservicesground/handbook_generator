# 🚀 Setup Guide - AI Handbook Generator

Complete setup instructions for running the AI Handbook Generator application.

---

## 📋 Prerequisites

- **Python**: 3.9 or higher
- **Grok API Key**: From [x.ai](https://x.ai)
- **Supabase Account**: Free tier from [supabase.com](https://supabase.com) (optional, LightRAG will work without it)
- **Git**: For cloning the repository

---

## 📥 Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SilverAI-Assignment-AI-Engineering
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If you encounter any issues, install packages individually:

```bash
pip install gradio requests python-dotenv
pip install PyPDF2 pdfplumber
pip install lightrag-hku supabase
pip install numpy torch transformers tqdm
pip install openai tiktoken
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the template
cp env_template.txt .env
```

Edit `.env` with your credentials:

```env
# Required: Grok API Configuration
GROK_API_KEY=your_actual_grok_api_key_here
GROK_API_BASE=https://api.x.ai/v1

# Optional: Supabase Configuration (LightRAG can work without it)
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# LightRAG Configuration (defaults are fine)
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIM=1536

# Application Settings (defaults are fine)
MAX_CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_HANDBOOK_LENGTH=20000
```

---

## 🔑 Getting API Keys

### Grok API Key (Required)

1. Go to [x.ai](https://x.ai) or [console.x.ai](https://console.x.ai)
2. Sign up / Log in
3. Navigate to API keys section
4. Create a new API key
5. Copy and paste into `.env` file

### Supabase (Optional)

1. Go to [supabase.com](https://supabase.com)
2. Create a new project (free tier is fine)
3. Go to Project Settings → API
4. Copy the **Project URL** and **anon/public** key
5. Paste into `.env` file

**Note**: LightRAG can work with local storage if you don't configure Supabase.

---

## ▶️ Running the Application

### Start the Application

```bash
python app.py
```

You should see:

```
============================================================
AI Handbook Generator - Starting...
============================================================
✅ Services initialized successfully!

🌐 Launching web interface...
Running on local URL:  http://0.0.0.0:7860
```

### Access the Interface

Open your browser and navigate to:

```
http://localhost:7860
```

---

## 📚 How to Use

### Step 1: Upload PDFs

1. Click the **"Upload PDF"** button
2. Select one or more PDF files
3. Wait for processing confirmation
4. You'll see the file listed in "Uploaded Files"

### Step 2: Ask Questions (Q&A Mode)

Simply type questions about your uploaded documents:

```
"What are the main findings?"
"Summarize the methodology section"
"What is RAG?"
```

### Step 3: Generate Handbook

Request a comprehensive handbook:

```
"Create a handbook on Retrieval-Augmented Generation"
"Generate a comprehensive guide about the uploaded papers"
"Write a manual on Machine Learning based on these documents"
```

The system will:
- Detect the handbook request
- Generate an outline
- Write each section (takes 5-10 minutes)
- Return a 20,000+ word structured document

---

## 🔧 Troubleshooting

### Issue: "Missing required environment variables"

**Solution**: Ensure `.env` file exists with valid `GROK_API_KEY`

```bash
# Check if .env exists
ls -a | grep .env

# Verify contents
cat .env
```

### Issue: "Error processing PDF"

**Solutions**:
- Ensure PDF is not password-protected
- Try a different PDF
- Check if PDF contains actual text (not just images)

### Issue: "Module not found" errors

**Solution**: Reinstall requirements

```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: LightRAG Installation Problems

**Solution**: Install from GitHub directly

```bash
pip install git+https://github.com/HKUDS/LightRAG.git
```

### Issue: Torch/PyTorch Installation

**For CPU-only** (smaller download):
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**For GPU** (CUDA 11.8):
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Issue: Grok API Rate Limits

**Solution**: The code includes retry logic with exponential backoff. If you hit rate limits:
- Wait a few minutes between requests
- Reduce concurrent generation attempts
- Check your API quota

---
```

---

## 📊 Expected Performance

- **PDF Processing**: 1-5 seconds per document
- **Q&A Response**: 2-5 seconds
- **Handbook Generation**: 5-15 minutes (for 20,000 words)
  - Outline generation: ~30 seconds
  - Per section: ~30-60 seconds
  - Total sections: typically 15-25

---

## 🐛 Debug Mode

For verbose logging, modify `app.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📝 Project Structure

```
SilverAI-Assignment-AI-Engineering/
├── app.py                  # Main Gradio application
├── config.py               # Configuration management
├── pdf_processor.py        # PDF extraction and chunking
├── grok_handler.py         # Grok API wrapper
├── rag_manager.py          # LightRAG integration
├── handbook_generator.py   # LongWriter implementation
├── requirements.txt        # Python dependencies
├── .env                    # Your API keys (create this)
├── env_template.txt        # Template for .env
├── SETUP.md               # This file
├── uploads/               # Temporary PDF storage
└── cache/                 # LightRAG cache directory
```

---

## ⚙️ Advanced Configuration

### Adjust Chunk Size

In `.env`:
```env
MAX_CHUNK_SIZE=1500
CHUNK_OVERLAP=300
```

### Change Handbook Length

In `.env`:
```env
MAX_HANDBOOK_LENGTH=30000
```

### Use Different Models

Modify `config.py`:
```python
GROK_MODEL = 'grok-beta'  # or other available models
```

---

## 🎯 Success Criteria Checklist

- [ ] Application starts without errors
- [ ] Can upload PDF documents
- [ ] PDF text is extracted and displayed in status
- [ ] Can ask questions and receive contextual answers
- [ ] Can request handbook generation
- [ ] Handbook generates with 20,000+ words
- [ ] Handbook has proper structure (headings, sections)
- [ ] Handbook references uploaded PDF content

---

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all API keys are correct
3. Ensure Python version is 3.9+
4. Check terminal output for specific error messages
5. Try running the test script

---

## 🎉 You're Ready!

If you've completed all steps above, you should have a working AI Handbook Generator.

**Quick Start Command:**
```bash
python app.py
```

Then open `http://localhost:7860` in your browser.

Happy handbook generating! 📚✨
