# FIDIC Red Book 1999 - RAG Document Preparation

A streamlined PDF-to-text extraction project to prepare FIDIC Red Book 1999 documentation for RAG (Retrieval-Augmented Generation) applications.

## Project Status: ✅ Ready for RAG

**Progress**: PDF successfully extracted to structured markdown format, optimized for embedding and retrieval.

## 📁 Project Structure

```
construction-legal-ai/
├── README.md                          # This file
├── pyproject.toml                     # Project dependencies (uv)
├── uv.lock                           # Dependency lock file
├── src/
│   └── pdf_parser.py                 # PyMuPDF-based PDF extractor
├── docs/
│   └── TECHNICAL_ANALYSIS.md         # Detailed technical documentation
├── FIDIC-Red-Book-1999.pdf          # Source PDF (128 pages)
└── FIDIC-Red-Book-1999.md           # Extracted markdown (PRIMARY RAG SOURCE)
```

## 🎯 Primary Output for RAG

**File**: `FIDIC-Red-Book-1999.md` (102KB)

**Why this format is ideal for RAG:**
- ✅ **Structured headers**: Each page marked with `# Page X` for easy chunking
- ✅ **Clean text**: Plain text with minimal formatting overhead
- ✅ **Metadata-friendly**: Page numbers easily extractable for source attribution
- ✅ **Embedding-ready**: Works seamlessly with OpenAI, Cohere, or HuggingFace embeddings
- ✅ **Lightweight**: 102KB (~25,000 words) for efficient vector storage

**Content Coverage:**
- Pages 1-9: Front matter (Title, Errata, Acknowledgements, Foreword)
- Pages 10-90: Empty (reserved page numbers for print formatting)
- Pages 91-128: Guidance for Particular Conditions, Forms, and Annexes

## ⚠️ Important Note: Document Content

The extracted PDF contains **Guidance and Forms**, NOT the actual General Conditions.

**What's Included:**
- ✅ Guidance for modifying contract clauses
- ✅ Sample forms (Letter of Tender, Contract Agreement, etc.)
- ✅ Annexes A-G (Security/Guarantee templates)

**What's Missing:**
- ❌ General Conditions - The actual contract text (Clauses 1-20)
  - e.g., Full definitions in "1.1 Definitions"
  - e.g., Complete obligations in "4.1 Contractor's General Obligations"

**For complete RAG coverage**, you would need:
- The actual General Conditions document (separate FIDIC publication)
- Or supplement with FIDIC Yellow/Silver Book variants

## 🚀 Quick Start

### Prerequisites
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Python 3.14 managed by uv
```

### Setup
```bash
# Initialize project
uv sync

# Verify Python version
uv run python --version
# Output: Python 3.14.x
```

### Extract PDF to Markdown
```bash
uv run python src/pdf_parser.py
```

**Output:**
- `FIDIC-Red-Book-1999.md` - Markdown format with page headers ✅

## 📊 RAG Implementation Guide

### Recommended Chunking Strategy

```python
# 1. Load the markdown file
with open('FIDIC-Red-Book-1999.md', 'r') as f:
    content = f.read()

# 2. Split by page headers
pages = content.split('# Page ')

# 3. Filter empty pages (10-90)
valid_pages = [
    page for page in pages
    if len(page.strip()) > 50  # Skip nearly empty pages
]

# 4. Create chunks with metadata
chunks = []
for page in valid_pages:
    lines = page.split('\n', 1)
    page_num = lines[0].strip()
    text = lines[1] if len(lines) > 1 else ""

    chunks.append({
        'text': text,
        'metadata': {
            'page': page_num,
            'source': 'FIDIC-Red-Book-1999',
            'section': determine_section(page_num)  # Guidance/Forms/Annexes
        }
    })

# 5. Generate embeddings and store in vector DB
# (Use your preferred embedding model and vector store)
```

### Metadata Enrichment

```python
def determine_section(page_num):
    """Map page numbers to document sections"""
    page = int(page_num)
    if page <= 9:
        return "Front Matter"
    elif 91 <= page <= 112:
        return "Guidance for Particular Conditions"
    elif 113 <= page <= 120:
        return "Annexes (Security Forms)"
    elif 121 <= page <= 128:
        return "Sample Forms (Tender/Agreement)"
    else:
        return "Reserved Pages"
```

### Sample Vector DB Configuration

```python
# Example with Pinecone
from pinecone import Pinecone
from openai import OpenAI

# Initialize
pc = Pinecone(api_key="your-key")
index = pc.Index("fidic-contracts")
client = OpenAI()

# Embed and upsert chunks
for i, chunk in enumerate(chunks):
    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk['text']
    ).data[0].embedding

    index.upsert(vectors=[(
        f"fidic-page-{chunk['metadata']['page']}",
        embedding,
        chunk['metadata']
    )])
```

## 🛠️ Technical Stack

- **Language**: Python 3.14
- **Package Manager**: uv (modern, fast, reliable)
- **PDF Library**: PyMuPDF (`pymupdf>=1.26.6`)
- **Output Format**: Markdown (UTF-8)

### Dependencies

```toml
# pyproject.toml
[project]
name = "construction-legal-ai"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = [
    "pymupdf>=1.26.6",
]
```

## 📖 Document Statistics

| Metric | Value |
|--------|-------|
| Total Pages | 128 |
| File Size (PDF) | 4.0 MB |
| File Size (Markdown) | 102 KB |
| Word Count | ~25,000 words |
| Content Pages | ~47 pages (excluding empty pages) |
| Character Count | ~104,000 characters |

## 🎓 Use Cases

### 1. Contract Q&A System
```
User: "What documents are required for a tender security?"
RAG: Retrieves Annex B (Tender Security form) + guidance
```

### 2. Clause Modification Advisor
```
User: "How should I modify payment terms for local currency?"
RAG: Retrieves Clause 14 guidance + examples
```

### 3. Document Template Generator
```
User: "Generate a Letter of Tender for building project"
RAG: Retrieves sample form + fills in placeholders
```

### 4. Compliance Checker
```
User: "Is my performance security format FIDIC-compliant?"
RAG: Retrieves Annexes C & D + compares structure
```

## 🔄 Regenerating Outputs

If you need to re-extract from the PDF:

```bash
# Run the parser
uv run python src/pdf_parser.py

# Output will be generated at project root
ls -lh FIDIC-Red-Book-1999.md
```

## 📚 Additional Resources

- **FIDIC Official**: [fidic.org](https://fidic.org)
- **Original Document**: FIDIC Red Book 1999 (ISBN 2-88432-022-9)
- **Technical Analysis**: See `docs/TECHNICAL_ANALYSIS.md`
- **RAG Frameworks**: LangChain, LlamaIndex, Haystack

## 🧹 Project Cleanup Notes

**Recent Optimizations (2025-11-16):**
- ❌ Removed redundant outputs (`.txt`, `.html` formats)
- ❌ Removed duplicate parsers (`pdf_extractor.py`)
- ❌ Removed structured JSON files (not needed for basic RAG)
- ✅ Single source of truth: `FIDIC-Red-Book-1999.md`
- ✅ Simplified codebase: One parser, one output
- 💾 Storage saved: ~9.4 MB

## 🤝 Contributing

This project is designed for:
- ✅ Academic research on construction contracts
- ✅ RAG/LLM application development
- ✅ Legal tech prototyping

**Note**: FIDIC Red Book content is copyrighted by FIDIC. This tool is for authorized use only.

## 📋 Next Steps

### For RAG Implementation:
1. ✅ Load `FIDIC-Red-Book-1999.md`
2. ✅ Chunk by pages (filter empty pages 10-90)
3. ✅ Generate embeddings (OpenAI/Cohere/HuggingFace)
4. ✅ Store in vector DB (Pinecone/Weaviate/Chroma)
5. ✅ Build query interface

### For Complete Coverage:
- [ ] Obtain FIDIC General Conditions (Clauses 1-20 full text)
- [ ] Extract other FIDIC variants (Yellow/Silver Book)
- [ ] Add construction case law for legal context
- [ ] Include project-specific Particular Conditions examples

## 📄 License

This parser tool is for academic/research purposes.

**Copyright Notice**: FIDIC Red Book content is copyrighted by FIDIC (Fédération Internationale des Ingénieurs-Conseils). Ensure you have proper licensing for commercial use.

---

**Last Updated**: 2025-01-16
**Status**: ✅ Production-ready for RAG applications
**Primary Output**: `FIDIC-Red-Book-1999.md` (102KB markdown)
