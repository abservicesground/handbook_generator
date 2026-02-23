# 📚 AI Handbook Generator

> **LunarTech AI Engineering Assignment**  
> A chat application that generates comprehensive 20,000-word handbooks from PDF documents using RAG and LongWriter techniques.

---

## 🎯 Project Overview

This application allows users to:
- 📄 **Upload PDF documents** (research papers, documentation, textbooks)
- 💬 **Chat and ask questions** about the uploaded content using RAG
- 📖 **Generate comprehensive handbooks** (20,000+ words) through conversational requests

### Key Features

✅ **PDF Processing** - Extracts and chunks text from PDFs  
✅ **Knowledge Graph** - Uses LightRAG for semantic retrieval  
✅ **Contextual Q&A** - RAG-powered question answering  
✅ **Long-form Generation** - LongWriter technique for 20k+ word documents  
✅ **Chat Interface** - Simple, intuitive Gradio UI  
✅ **Structured Output** - Handbooks with TOC, sections, and proper formatting

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Handbook Generator                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User Input → PDF Upload → Text Extraction → Chunking      │
│                    ↓                                        │
│            LightRAG Knowledge Graph                         │
│                    ↓                                        │
│      User Query → Context Retrieval → Grok API             │
│                    ↓                                        │
│              Q&A Response / Handbook                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Gradio | Chat interface and PDF upload |
| **LLM** | Grok 4.1 (xAI) | Response generation |
| **RAG** | LightRAG | Knowledge graph and retrieval |
| **PDF Processing** | PyPDF2, pdfplumber | Text extraction |
| **Backend** | Python 3.9+ | Application logic |
| **Storage** | Local cache | Document and embedding storage |

---

## 📁 Project Structure

```
SilverAI-Assignment-AI-Engineering/
│
├── app.py                      # Main Gradio application
├── config.py                   # Configuration and environment management
├── pdf_processor.py            # PDF text extraction and chunking
├── grok_handler.py            # Grok API wrapper
├── rag_manager.py             # LightRAG integration
├── handbook_generator.py      # LongWriter implementation
│
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create from template)
├── env_template.txt          # Template for environment setup
├── .gitignore                # Git ignore rules
│
├── SETUP.md                  # Detailed setup instructions
├── DEMO_GUIDE.md            # Demo creation guide
├── PROJECT_README.md        # This file
├── test_system.py           # System test script
│
├── uploads/                 # Temporary PDF storage (auto-created)
├── cache/                   # LightRAG cache (auto-created)
│
└── LongWriter-main/         # Reference implementation (provided)
    └── agentwrite/
        ├── plan.py          # Planning logic reference
        └── write.py         # Writing logic reference
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Grok API key from [x.ai](https://x.ai)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd SilverAI-Assignment-AI-Engineering

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env_template.txt .env
# Edit .env and add your GROK_API_KEY

# Run application
python app.py
```

### Access

Open browser to: `http://localhost:7860`

---

## 📖 Usage Guide

### 1. Upload Documents

1. Click **"Upload PDF"** button
2. Select PDF file(s)
3. Wait for processing confirmation
4. See file listed in "Uploaded Files"

### 2. Ask Questions (Q&A Mode)

Type questions about your documents:

```
"What are the main findings?"
"Explain the methodology used"
"Summarize the key concepts"
```

System retrieves relevant context using LightRAG and generates responses using Grok.

### 3. Generate Handbook

Request a comprehensive handbook:

```
"Create a handbook on Machine Learning"
"Generate a comprehensive guide about RAG systems"
"Write a manual on the uploaded research"
```

**System Process:**
1. Detects handbook request
2. Generates detailed outline (~20 sections)
3. Retrieves relevant context for each section
4. Writes each section iteratively (LongWriter technique)
5. Returns 20,000+ word structured document

**Time:** 5-15 minutes depending on complexity

---

## 🧠 Technical Implementation

### LongWriter Technique

Based on the research paper in `Documentation/`, the system uses a **plan-then-write** approach:

1. **Planning Phase**
   - Generate comprehensive outline
   - Break topic into 15-25 sections
   - Allocate ~1000 words per section

2. **Writing Phase**
   - Iterate through each section
   - Retrieve relevant context from knowledge graph
   - Generate section with awareness of previous content
   - Maintain consistency and avoid repetition

3. **Assembly Phase**
   - Combine all sections
   - Add table of contents
   - Format with proper headings
   - Validate word count (20,000+ target)

### RAG Implementation

**Document Ingestion:**
```python
PDF → Extract Text → Chunk (1000 words, 200 overlap)
  → Generate Embeddings → Store in LightRAG
```

**Query Processing:**
```python
User Query → Embed Query → Retrieve Top-K Chunks
  → Assemble Context → Send to LLM → Generate Response
```

### Key Modules

#### `pdf_processor.py`
- Extracts text from PDFs using multiple methods
- Intelligent text cleaning
- Smart chunking with overlap
- Metadata extraction

#### `grok_handler.py`
- Wraps Grok API calls
- Implements retry logic with exponential backoff
- Context-aware generation
- Error handling

#### `rag_manager.py`
- Initializes LightRAG
- Manages document storage
- Handles asynchronous operations
- Provides context retrieval

#### `handbook_generator.py`
- Implements LongWriter technique
- Detects handbook requests
- Generates outlines
- Writes sections iteratively
- Manages generation progress

#### `app.py`
- Gradio interface
- Orchestrates all components
- Handles user interactions
- Manages state

---

## 🔧 Configuration

### Environment Variables

Required in `.env`:

```env
# Grok API (Required)
GROK_API_KEY=your_key_here
GROK_API_BASE=https://api.x.ai/v1

# Optional Configuration
EMBEDDING_MODEL=text-embedding-3-small
MAX_CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_HANDBOOK_LENGTH=20000
```

### Customization

**Adjust chunking:**
```python
pdf_processor = PDFProcessor(chunk_size=1500, chunk_overlap=300)
```

**Change generation temperature:**
```python
grok.generate_response(prompt, temperature=0.5)  # More focused
```

**Modify handbook length:**
```python
handbook_gen.generate_handbook(topic, target_length=30000)
```

---

## 🧪 Testing

### Run System Test

```bash
python test_system.py
```

Tests:
- ✅ Configuration loading
- ✅ PDF processing
- ✅ Grok API connection
- ✅ RAG manager initialization
- ✅ Handbook detection

### Manual Testing

1. **PDF Upload Test:**
   - Upload sample PDF
   - Verify extraction in status message
   - Check "Uploaded Files" list

2. **Q&A Test:**
   - Ask simple question
   - Ask complex question
   - Verify contextual responses

3. **Handbook Test:**
   - Request handbook on specific topic
   - Monitor generation progress
   - Verify 20,000+ word output
   - Check structure and formatting

---

## 📊 Performance

### Expected Metrics

| Operation | Time | Notes |
|-----------|------|-------|
| PDF Upload | 1-5s | Depends on file size |
| Q&A Response | 2-5s | Single query |
| Handbook Generation | 5-15m | ~20-30 API calls |
| Section Generation | 30-60s | Per section |

### Resource Usage

- **Memory:** ~2-4 GB (LightRAG + embeddings)
- **Storage:** ~100 MB per 100 pages of PDFs
- **API Calls:** ~25-35 per handbook generation

---

## 🐛 Troubleshooting

### Common Issues

**"Missing required environment variables"**
- Solution: Create `.env` file with `GROK_API_KEY`

**"Error processing PDF"**
- Solution: Ensure PDF is text-based (not scanned image)

**"LightRAG import error"**
- Solution: `pip install lightrag-hku`

**"Torch not found"**
- Solution: `pip install torch` (CPU version is fine)

See `SETUP.md` for detailed troubleshooting.

---

## 📝 Assignment Compliance

### Requirements Met

✅ **PDF Upload** - Accepts and parses PDF files  
✅ **Knowledge Graph** - LightRAG stores content  
✅ **Chat Interface** - Gradio text input/output  
✅ **Contextual Responses** - RAG retrieval working  
✅ **Handbook Generation** - 20,000+ words via chat  
✅ **Proper Structure** - TOC, headings, sections  
✅ **LongWriter Technique** - Plan-then-write implementation  
✅ **Grok 4.1 Integration** - Primary LLM  
✅ **Working Demo** - Full application functional

### Test Case (from README.md)

**Input:**
- Upload 2-3 AI-related PDFs
- Chat: "Create a handbook on Retrieval-Augmented Generation"

**Expected Output:**
- 20,000+ word structured document ✅
- Table of contents ✅
- Sections with proper headings ✅
- Citations from uploaded PDFs ✅

---

## 📦 Deliverables

### Code
- ✅ Complete Python application
- ✅ Modular, well-structured code
- ✅ Configuration management
- ✅ Error handling

### Documentation
- ✅ `SETUP.md` - Installation instructions
- ✅ `DEMO_GUIDE.md` - Demo creation guide
- ✅ `PROJECT_README.md` - This file
- ✅ Inline code comments
- ✅ Test script

### Demo
- Create video or screenshots following `DEMO_GUIDE.md`
- Show: Upload → Q&A → Handbook generation
- Prove: 20,000+ word output

---

## 🔒 Notes

- API keys stored in `.env` (not committed)
- Cache directory excluded from git
- PDF uploads temporary (can be cleared)
- LightRAG stores data locally

---

## 📧 Submission

**To:** tk.lunartech@gmail.com

**Include:**
1. GitHub repository link (or .zip)
2. SETUP.md instructions
3. Demo video OR screenshots
4. Brief write-up (approach, challenges, solutions)

---

## 🎓 Learning Outcomes

This project demonstrates:
- 🔹 **AI Engineering** - Integrating multiple AI services
- 🔹 **RAG Systems** - Knowledge graph creation and retrieval
- 🔹 **LLM Integration** - Grok API usage and prompt engineering
- 🔹 **Long-form Generation** - LongWriter technique implementation
- 🔹 **Full-stack Development** - Backend logic + UI
- 🔹 **Software Engineering** - Modular design, error handling, testing

---

## 🙏 Acknowledgments

- **LunarTech** - Assignment and resources
- **LongWriter Research** - Paper and reference implementation
- **LightRAG** - Knowledge graph framework
- **xAI** - Grok API
- **Gradio** - UI framework

---

## 📄 License

This project is for educational and evaluation purposes as part of the LunarTech AI Engineering assignment.

---

**Built with 🤖 AI assistance (as encouraged by the assignment guidelines)**

_For questions or issues, refer to SETUP.md or contact through submission email._
