# 📚 Document Intelligence Platform

A full-stack RAG (Retrieval-Augmented Generation) application that scrapes book data, generates AI insights, and allows users to query the dataset using natural language.

## 🚀 Setup Instructions

### Backend (Django)
1. Navigate to `/backend`
2. Create a `.env` file with `OPENROUTER_API_KEY=your_key_here`
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start the scraper: `python run_scraper.py`
6. Run server: `python manage.py runserver`

### Frontend (Next.js)
1. Navigate to `/frontend`
2. Install dependencies: `npm install`
3. Run dev server: `npm run dev`

## 🛠️ Tech Stack
- **Backend:** Django REST Framework, MySQL, ChromaDB (Vector Store)
- **AI:** OpenRouter (Mistral 7B), Sentence-Transformers (Embeddings)
- **Automation:** Selenium (Headless Chrome)
- **Frontend:** Next.js, Tailwind CSS, Lucide React

## 📖 API Endpoints
- `GET /api/books/` - List all scraped books
- `POST /api/chat/` - RAG Query endpoint for AI Q&A
