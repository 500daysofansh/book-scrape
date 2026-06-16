import os
import django
import json
from dotenv import load_dotenv

# 1. Initialize Django Environment
# This allows the script to interact with your MySQL models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Import your custom modules
from books.models import Book
from books.scraper import scrape_books
from books.ai_insights import generate_book_insights
from books.rag_pipeline import add_to_rag_storage

def run_integration_pipeline():
    """
    Main execution pipeline: 
    1. Scrapes real data 
    2. Generates AI insights 
    3. Saves to MySQL 
    4. Indexes in Vector DB
    """
    print("🚀 Starting Document Intelligence Pipeline...")
    
    # Load environment variables (API Keys)
    load_dotenv()

    # Step 1: Scrape real book data (Clicks into pages for full descriptions)
    # We set a limit of 10 to ensure we get a good variety for the RAG system
    scraped_books = scrape_books(limit=10)
    
    if not scraped_books:
        print("❌ No books were scraped. Check your internet or Selenium setup.")
        return

    for data in scraped_books:
        try:
            print(f"\n--- Processing: {data['title']} ---")
            
            # Step 2: Generate AI Insights (Summary, Genre, and Sentiment)
            # This fulfills the 'AI Insight Generation' requirement
            print("🧠 Requesting AI insights from OpenRouter...")
            insights = generate_book_insights(data['description'])
            
            # Step 3: Save to MySQL Database
            # We use update_or_create to prevent duplicate entries on re-runs
            book, created = Book.objects.update_or_create(
                url=data['url'],
                defaults={
                    'title': data['title'],
                    'author': data['author'],
                    'rating': data['rating'],
                    'description': data['description'],
                    'summary': insights.get('summary', 'No summary available.'),
                    'genre': insights.get('genre', 'General'),
                    'sentiment': insights.get('sentiment', 'Neutral') # Fix: Population of sentiment field
                }
            )
            
            status = "Created" if created else "Updated"
            print(f"💾 MySQL: {status} record for '{book.title}'")

            # Step 4: Index for RAG (ChromaDB)
            # This enables the 'Intelligent Querying' requirement
            print("🔢 Generating embeddings and indexing in ChromaDB...")
            add_to_rag_storage(book)
            
            print(f"✅ Successfully processed: {book.title}")

        except Exception as e:
            print(f"⚠️ Error processing {data.get('title', 'Unknown Book')}: {e}")
            continue

    print("\n🏁 Pipeline complete. Your system is now populated with intelligent data!")

if __name__ == "__main__":
    run_integration_pipeline()