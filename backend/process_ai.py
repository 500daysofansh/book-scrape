import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from books.models import Book
from books.ai_logic import process_book_for_rag

def start_intelligence():
    books = Book.objects.all()
    print(f"🧠 Processing {len(books)} books for AI...")
    for book in books:
        process_book_for_rag(book)
    print("✅ All books indexed in Vector DB!")

if __name__ == "__main__":
    start_intelligence()