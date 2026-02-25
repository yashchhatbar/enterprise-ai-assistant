
# 🚀 Enterprise AI Knowledge Assistant (RAG-Based Internal ChatGPT)

## 📌 Overview
This is a **production-ready Enterprise AI Knowledge Assistant** designed to securely query internal company documents using Retrieval-Augmented Generation (RAG). It leverages **Google Gemini** for embeddings and LLM, **FAISS** for vector search, **FastAPI** for the backend, and **Streamlit** for the frontend.

**Key Features:**
- **Secure Document Upload**: Supports PDF, DOCX, TXT, CSV.
- **RAG Architecture**: Retrieves context from uploaded documents to answer queries accurately.
- **Privacy First**: Strict system prompts prevent hallucinations; API keys stored securely.
- **Free Deployment**: Can be deployed 100% free on Render/Railway and Streamlit Cloud.
- **Dockerized**: Includes production-ready Docker setup.

---

## 🏗 System Architecture

```ascii
User  --->  [Streamlit UI]  --->  [FastAPI Backend]
                                     |
                                     v
                            [Document Processor]
                                     |
                                     v
[Gemini API] <--- (Embeddings) <--- [Chunker]
      ^                              |
      |                              v
(Generation) <--- [RAG Chain] <--- [FAISS Vector DB]
```

---

## ⚙️ Setup & Installation

### 1️⃣ Prerequisites
- Python 3.9+
- Docker (optional)
- Google Gemini API Key ([Get it here](https://aistudio.google.com/app/apikey))

### 2️⃣ Environment Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/enterprise-ai-assistant.git
   cd enterprise-ai-assistant
   ```
2. Create `.env` file from example:
   ```bash
   cp .env.example .env
   ```
3. Add your `GOOGLE_API_KEY` to the `.env` file.

### 3️⃣ Run Locally (Docker) - Recommended
```bash
docker-compose up --build
```
- Frontend: [http://localhost:8501](http://localhost:8501)
- Backend API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4️⃣ Run Locally (Manual)
**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
**Frontend:**
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## 🌍 Free Deployment Guide

### 1️⃣ Backend Deployment (Render.com)
1. Push this code to GitHub.
2. Sign up on [Render](https://render.com/).
3. Create a **New Web Service**.
4. Connect your repository.
5. Settings:
   - **Root Directory**: `.` (current directory)
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**: Add `GOOGLE_API_KEY`.
6. Deploy! Copy the **Render URL** (e.g., `https://my-backend.onrender.com`).

### 2️⃣ Frontend Deployment (Streamlit Community Cloud)
1. Sign up on [Streamlit Cloud](https://streamlit.io/cloud).
2. Connect your GitHub repository.
3. Settings:
   - **Main file path**: `frontend/app.py`
   - **Requirements file**: `frontend/requirements.txt` (Streamlit might detect it automatically, or pick root. Ensure correct path).
4. **Advanced Settings (Secrets)**:
   - Add `API_URL = "https://my-backend.onrender.com"` (Your Render Backend URL)
5. Deploy!

---

## 🎓 Technical Explanation (Interview / Resume)

### How RAG Works
1. **Ingestion**: Documents are split into overlapping chunks (1000 chars, 200 overlap) to preserve context.
2. **Embedding**: Each chunk is converted into a vector using **Gemini Embeddings**.
3. **Storage**: Vectors are stored in **FAISS** (Facebook AI Similarity Search) for efficient similarity search.
4. **Retrieval**: When a user asks a question, it is also converted to a vector. We find the top 4 most similar chunks in FAISS.
5. **Generation**: The retrieved chunks + strict system prompt + user question are sent to the **Gemini LLM** to generate an accurate answer based *only* on the sources.

### Design Decisions
- **FAISS**: Chosen for local, fast, and free vector storage without needing an external database like Pinecone (though Pinecone is better for scaling).
- **Gemini**: Used for its cost-effectiveness (free tier available) and high performance in both embeddings and generation.
- **FastAPI**: Provides asynchronous, high-performance API endpoints, essential for handling multiple concurrent upload/query requests.

### Scaling to 1M+ Documents
To scale this SaaS:
1. **Database**: Switch FAISS (in-memory) to **Pinecone** or **Milvus** (managed vector DB).
2. **Storage**: Store raw files in **AWS S3** instead of local disk.
3. **Queue**: Use **Celery + Redis** for processing large document uploads asynchronously.
4. **Auth**: Implement **JWT Authentication** to segregate user data (Multi-tenancy).

---

## 💰 Cost Estimation (Google Gemini)
- **Free Tier**: 60 QPM (Queries Per Minute) - Sufficient for MVP/Demo.
- **Paid Tier**: $0.000125 / 1K characters (Input), $0.000375 / 1K characters (Output).
- **Deployment**: Render/Streamlit provide generous free tiers.
**Total Monthly Cost for MVP:** **$0.00**

---

### 📂 Folder Structure
```
enterprise-ai-assistant/
├── backend/            # FastAPI App & RAG Logic
├── frontend/           # Streamlit UI
├── Dockerfile          # Multi-stage build
├── docker-compose.yml  # Container orchestration
└── README.md           # Documentation
```

🚀 **Ready for Production!**
