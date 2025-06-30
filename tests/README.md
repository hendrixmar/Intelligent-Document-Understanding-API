# 📄 Intelligent Document Understanding API

An end-to-end API that extracts structured data from unstructured documents using OCR, semantic search, and LLMs. This project processes image/PDF documents and returns clean, structured JSON with recognized entities.

---

## 🚀 Project Overview

This repository is the solution for the AI/ML Developer Coding Challenge focused on Intelligent Document Understanding. It combines:

- 📷 Optical Character Recognition (EasyOCR, Tesseract)
- 🔍 Document classification via category detection with LLM 
- 🤖 Entity extraction via Large Language Models (OpenAI, Llama2, etc.)
- 🧠 Structured response parsing into standardized JSON

---

## 🧱 Architecture

```mermaid
graph TD
    A[User Upload: PDF/Image] --> B[Preprocessing]
    B --> C[OCR (EasyOCR)]
    C --> D[Semantic Splitting]
    D --> E[Vector DB (Weaviate)]
    E --> F[Document Type Matching]
    C --> G[LLM Entity Extraction]
    F --> G
    G --> H[Standardized JSON Output]
```

---

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/hendrixmar/Intelligent-Document-Understanding-API
cd Intelligent-Document-Understanding-API
```

2. **Install dependencies**

You can start the project with docker using this command:

```bash
docker compose up --build
```
this will expose the following endpoints.

### Swagger documentation
- http://localhost:8000/api/docs#/

### Frontend for testing the API
- http://localhost:8501/api/docs



## ⚙️ Configuration

Create a `.env` file for API keys (if using OpenAI or any LLM service):
```env
RAG_OPENAI_API_KEY=your-api-key-here
```

Optional configuration values can include vector DB settings, file upload limits, and OCR thresholds.

---

## 📑 Usage

### 🔄 PDF/Image to JSON Pipeline Test

To process a single PDF and get structured JSON output:
```bash

```

This will:

- Convert PDF to images
- Preprocess each page
- Run OCR with EasyOCR
- Extract entities with LLM
- Print final JSON output

---

## 🧪 Testing Procedures

- Unit tests: `tests/test_ocr.py`, `tests/test_vector_search.py`
- Integration test with sample document
- Sample document set from [Real World Documents Kaggle Dataset](https://www.kaggle.com/datasets/realworlddocuments)

---

## 📌 Features

- EasyOCR with custom preprocessing (grayscale, denoise, threshold)
- Multi-page PDF support
- Document type detection via vector DB
- Entity extraction using custom LLM prompts
- Async processing 
- JSON output standardization

---


---

## 🏆 Bonus Features

- [x] Low-quality text handling via preprocessing
- [x] Web UI with streamlit
- [x] Docker support
- [] Integrations test
- [] Confidence scoring for document type and entities

---

## 📚 Acknowledgements

- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [PyTesseract](https://github.com/h/pytesseract)
- [pdf2image](https://github.com/Belval/pdf2image)
- [Weaviate](https://github.com/weaviate/weaviate)
- [OpenAI API](https://platform.openai.com/)

---

## 📬 Contact

For any questions, feel free to open an issue or reach out at [hendrikuwabara@gmail.com].

---
