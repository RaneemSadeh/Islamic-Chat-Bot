# 🕌 Islamic RAG Chatbot - الشيخ البوت

<div align="center">

![Islamic Chatbot](https://img.shields.io/badge/Islamic-Chatbot-green?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTEyIDJDNi40OCAyIDIgNi40OCAyIDEyczQuNDggMTAgMTAgMTAgMTAtNC40OCAxMC0xMFMxNy41MiAyIDEyIDJ6bTAgMThjLTQuNDEgMC04LTMuNTktOC04czMuNTktOCA4LTggOCAzLjU5IDggOC0zLjU5IDgtOCA4eiIvPjwvc3ZnPg==)
![RAG Architecture](https://img.shields.io/badge/RAG-Powered-blue?style=for-the-badge)
![Arabic NLP](https://img.shields.io/badge/Arabic-NLP-orange?style=for-the-badge)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)

**An intelligent Islamic knowledge assistant powered by Retrieval-Augmented Generation (RAG)**

*Bridging centuries of Islamic scholarship with cutting-edge AI technology*

[Features](#-features) • [Architecture](#-architecture) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Contributing](#-contributing)

</div>

---

## 📖 About

**Islamic RAG Chatbot** is an advanced AI-powered assistant that provides authentic, source-verified answers to Islamic questions in Arabic. Unlike traditional chatbots that rely solely on pre-trained knowledge, our system retrieves information from verified Islamic sources and generates contextualized responses with proper citations.

### 🎯 What Makes This Special?

-  Authentic Sources: All answers derived from verified Islamic references
-  Full Traceability: Every response includes original text, source name, and page numbers
-  RAG Architecture: Combines retrieval and generation for accurate, grounded responses
-  Arabic-First: Native Arabic language processing and understanding
-  Modern UI/UX: Beautiful, responsive React interface designed for seamless interaction

---

##  Features

### Core Capabilities

✅ **Source-Verified Responses**
- Original text extraction from authentic Islamic sources
- Complete citation with reference name and page/URL
- Contextualized explanation tailored to user's question

✅ **Comprehensive Knowledge Base**
- القرآن الكريم (The Holy Quran)
- صحيح البخاري (Sahih al-Bukhari)
- صحيح مسلم (Sahih Muslim)
- إسلام ويب (IslamWeb)
- كتب ابن تيمية (Books of Ibn Taymiyyah)

✅ **Advanced NLP Processing**
- Arabic handwritten text recognition (OCR)
- Semantic search using Arabic embeddings (ARABERT/mBERT)
- Context-aware response generation

✅ **Professional Frontend**
- Real-time chat interface
- Source highlighting and citation display
- Responsive design for all devices
- Arabic RTL support

---

##  Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface (React)                   │
│                  Modern Chat UI with RTL Support             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RAG Engine Core                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Query      │  │  Retrieval   │  │  Generation  │      │
│  │  Embedding   │─▶│    Engine    │─▶│    (LLM)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Vector Database (ChromaDB/FAISS)                │
│     Embedded Text Chunks + Metadata (source, page, type)    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Knowledge Base Sources                     │
│   Quran  |   Hadith  |   IslamWeb  |   Manuscripts  │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Frontend**
-  React with TypeScript
-  Modern CSS/Tailwind for styling
-  Real-time state management
-  Arabic RTL support

**Backend (RAG Pipeline)**
-  Gemini API for LLM generation
-  Vector database for semantic search
-  Arabic embedding models (ARABERT/mBERT)
-  LangChain/LlamaIndex framework

**Data Processing**
-  High-resolution OCR for handwritten Arabic
-  Text chunking with overlap
-  Metadata preservation system
-  Continuous knowledge base updates

---

## 🚀 Getting Started

### Prerequisites

```bash
node >= 18.0.0
npm >= 9.0.0
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/islamic-rag-chatbot.git
cd islamic-rag-chatbot
```

2. **Install dependencies**
```bash
npm install
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Add your Gemini API key and other configurations
```

4. **Run the development server**
```bash
npm run dev
```

5. **Open your browser**
```
Navigate to http://localhost:3000
```

---

##  Usage

### Basic Query

```typescript
// Example: Ask a question in Arabic
User: "ما حكم الصلاة في أول الوقت؟"

// Response structure:
{
  originalText: "النص الأصلي من المصدر...",
  source: {
    name: "صحيح البخاري",
    page: "١٢٣",
    type: "حديث"
  },
  explanation: "شرح مفصل ومعاد صياغته..."
}
```

### API Integration

```typescript
import { generateResponse } from './services/geminiService';

const response = await generateResponse(userQuery, retrievedChunks);
```

---

## 🔧 Configuration

### Embedding Models

Configure Arabic embedding models in `config/embeddings.ts`:

```typescript
export const EMBEDDING_CONFIG = {
  model: 'arabert-base-v2',
  dimension: 768,
  similarity: 'cosine'
};
```

### Vector Database

Set up your vector database connection:

```typescript
export const VECTOR_DB_CONFIG = {
  type: 'chromadb', // or 'faiss', 'pinecone'
  host: 'localhost',
  port: 8000
};
```

---

## 📊 Data Sources

| Source | Type | Status | Records |
|--------|------|--------|---------|
| القرآن الكريم | Digital | ✅ Active | 6,236 verses |
| صحيح البخاري | Digital | ✅ Active | 7,563 hadiths |
| صحيح مسلم | Digital | ✅ Active | 7,190 hadiths |
| إسلام ويب | Web Scraping | ✅ Active | ~50,000 articles |
| كتب ابن تيمية | Manuscripts | 🔄 Processing | In progress |

---

## 🙏 Acknowledgments

- Islamic scholars and researchers for source verification
- Arabic NLP community for language models
- Open-source contributors to RAG frameworks
- The IslamWeb platform for digital resources

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ for the Islamic community
Raneem Sadeh

</div>
