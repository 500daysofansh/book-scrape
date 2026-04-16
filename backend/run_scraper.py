import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from books.models import Book
from books.scraper import scrape_books
from books.ai_insights import generate_book_insights
from books.rag_pipeline import add_to_rag_storage

def populate_and_intel():
    print("🕷️ Starting Scraper...")
    scraped_data = scrape_books(limit=5) # Start small to test
    
    for data in scraped_data:
        # 1. Generate AI Insights (Summary & Genre)
        print(f"🧠 Generating AI insights for: {data['title']}...")
        insights = generate_book_insights(data['description'])
        
        # 2. Save to MySQL
        book, created = Book.objects.update_or_create(
            url=data['url'],
            defaults={
                'title': data['title'],
                'rating': data['rating'],
                'description': data['description'],
                'author': data['author'],
                'summary': insights.get('summary', 'No summary'),
                'genre': insights.get('genre', 'General')
            }
        )
        
        # 3. Save to ChromaDB for RAG
        add_to_rag_storage(book)
        print(f"✅ Processed: {book.title}")

if __name__ == "__main__":
    populate_and_intel()