import os
import requests
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load API Key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize Local Models & Vector DB
# Using all-MiniLM-L6-v2: Small, fast, and great for sentence similarity
model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="books_rag")

def add_to_rag_storage(book_obj):
    """
    Requirement: Intelligent Querying & Vector Storage.
    Combines Title and Description to ensure the search finds specific books by name.
    """
    print(f"🔢 Indexing vector for: {book_obj.title}...")
    
    # IMPROVEMENT: Combine Title + Description for better search hit-rate
    searchable_content = f"BOOK TITLE: {book_obj.title}. DESCRIPTION: {book_obj.description}"
    
    # Generate embedding
    embedding = model.encode(searchable_content).tolist()
    
    # Upsert into ChromaDB (using update avoids duplicate ID errors)
    collection.upsert(
        ids=[str(book_obj.id)],
        embeddings=[embedding],
        documents=[searchable_content],
        metadatas=[{
            "title": book_obj.title, 
            "author": book_obj.author or "Classic Literature",
            "url": book_obj.url
        }]
    )

def query_rag_system(user_question):
    """
    Requirement: POST API for RAG-based Q&A.
    Retrieves top 4 relevant context pieces to avoid 'hallucinations'.
    """
    # 1. Convert user question to vector
    question_vector = model.encode(user_question).tolist()
    
    # 2. Search ChromaDB (Increased n_results to 4 for better context coverage)
    results = collection.query(query_embeddings=[question_vector], n_results=4)
    
    # Flatten results
    context_text = "\n\n---\n\n".join(results['documents'][0])
    metadata_list = results['metadatas'][0]
    
    # 3. Construct the "System" prompt for OpenRouter
    # This strict instruction prevents the AI from guessing if it doesn't know the answer
    prompt = f"""
    You are a professional Librarian AI. Use the provided book context to answer the user's question.
    
    CONTEXT FROM DATABASE:
    {context_text}
    
    USER QUESTION: 
    {user_question}
    
    STRICT RULES:
    1. Answer ONLY using the context provided above.
    2. If the answer is not in the context, say: "I'm sorry, I don't have information on that specific book in my database yet."
    3. Always mention the 'Title' of the book you are referencing.
    4. Keep the answer concise and professional.
    """
    
    # 4. Talk to OpenRouter
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-OpenRouter-Title": "Book Intelligence Platform"
    }
    
    payload = {
        "model": "openrouter/free", # Automatically uses the best available free model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2 # Lower temperature = more factual, less creative
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
            # Return answer and unique sources
            sources = list(set([m['title'] for m in metadata_list]))
            return {"answer": answer, "sources": sources}
        else:
            return {
                "answer": f"AI Service Error (Code {response.status_code}). Please check API credits.",
                "sources": []
            }
    except Exception as e:
        return {"answer": f"RAG System Error: {str(e)}", "sources": []}