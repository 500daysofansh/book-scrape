import os
import requests
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load API Key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize Local Models & Vector DB
# Using a local embedding model saves API costs and is faster for search
model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="books_rag")

def add_to_rag_storage(book_obj):
    """
    Generates embeddings for book description and stores in ChromaDB.
    """
    print(f"Indexing vector for: {book_obj.title}...")
    embedding = model.encode(book_obj.description).tolist()
    
    collection.add(
        ids=[str(book_obj.id)],
        embeddings=[embedding],
        documents=[book_obj.description],
        metadatas=[{
            "title": book_obj.title, 
            "author": book_obj.author or "Unknown",
            "url": book_obj.url
        }]
    )

# ... (Keep your imports and ChromaDB setup at the top)

def query_rag_system(user_question):
    question_vector = model.encode(user_question).tolist()
    results = collection.query(query_embeddings=[question_vector], n_results=2)
    context_text = "\n\n".join(results['documents'][0])
    metadata_list = results['metadatas'][0]
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-OpenRouter-Title": "Book Intel Platform"
    }
    
    prompt = f"Context: {context_text}\n\nQuestion: {user_question}\n\nRules: Answer based only on context and cite the book title."
    
    payload = {
        "model": "openrouter/free", # Changed to auto-router
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
            return {"answer": answer, "sources": [m['title'] for m in metadata_list]}
        else:
            return {"answer": f"AI Error: {response.status_code}", "sources": []}
    except Exception as e:
        return {"answer": f"System Error: {str(e)}", "sources": []}