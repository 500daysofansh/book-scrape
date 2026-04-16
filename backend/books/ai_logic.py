import chromadb
from sentence_transformers import SentenceTransformer
import requests
import json

# Initialize ChromaDB (Local persistent storage)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="books_collection")

# Initialize Embedding Model (Runs on your CPU)
model = SentenceTransformer('all-MiniLM-L6-v2')

def process_book_for_rag(book_obj):
    """Stores book description in ChromaDB for searching."""
    embedding = model.encode(book_obj.description).tolist()
    
    collection.add(
        ids=[str(book_obj.id)],
        embeddings=[embedding],
        metadatas=[{"title": book_obj.title, "url": book_obj.url}],
        documents=[book_obj.description]
    )
    print(f"Stored vector for: {book_obj.title}")

def generate_ai_insight(description):
    """Calls LM Studio to get a summary/genre."""
    url = "http://localhost:1234/v1/chat/completions" # Default LM Studio Port
    
    prompt = f"Analyze this book description. Provide a 1-sentence summary and a genre classification.\n\nDescription: {description}"
    
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()['choices'][0]['message']['content']
    except:
        return "AI Insight currently unavailable. (Is LM Studio running?)"