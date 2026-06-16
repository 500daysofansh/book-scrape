from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book, ChatHistory
from .serializers import BookSerializer
from .rag_pipeline import query_rag_system, collection
from .scraper import run_deep_scraper 
import json

# --- Requirement: POST API for Uploading/Processing ---
class ProcessBooksView(APIView):
    """
    Triggers the Selenium + AI Insight + ChromaDB pipeline.
    Connects the frontend 'Sync' button to the Python automation logic.
    """
    def post(self, request):
        try:
            run_deep_scraper() 
            return Response({
                "status": "success",
                "message": "Scraper executed. Books processed and AI insights generated."
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- 1. Dashboard: List all books ---
class BookListView(APIView):
    """
    Requirement: GET API to list all uploaded books.
    """
    def get(self, request):
        books = Book.objects.all().order_by('-created_at')
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

# --- 2. Detail Page: Get a single book's details ---
class BookDetailView(APIView):
    """
    Requirement: GET API to retrieve full details of a specific book.
    """
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

# --- 3. Recommendations: Vector Similarity ---
class RecommendView(APIView):
    """
    Requirement: AI-based recommendation logic using Vector Similarity search in ChromaDB.
    """
    def get(self, request, pk):
        try:
            target_book = Book.objects.get(pk=pk)
            
            # Query ChromaDB for top 4 similar book descriptions
            results = collection.query(
                query_texts=[target_book.description],
                n_results=4 
            )
            
            # Filter out the current book's ID and fetch others from MySQL
            similar_ids = [int(id) for id in results['ids'][0] if id != str(pk)]
            recommended = Book.objects.filter(id__in=similar_ids)
            
            serializer = BookSerializer(recommended, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": "Could not generate recommendations."}, status=status.HTTP_400_BAD_REQUEST)

# --- 4. RAG Chat: Q&A with Sources & Caching ---
class RAGQueryView(APIView):
    """
    Requirement: POST API for RAG-based Q&A.
    Bonus Point: Caching AI responses to avoid repeated calls.
    """
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({"error": "No question provided"}, status=400)
        
        # BONUS FEATURE: Check Cache First
        cached_chat = ChatHistory.objects.filter(question__iexact=question).first()
        if cached_chat:
            try:
                source_titles = json.loads(cached_chat.sources)
            except:
                source_titles = []
                
            referenced_books = Book.objects.filter(title__in=source_titles)
            book_data = BookSerializer(referenced_books, many=True).data
            
            return Response({
                "answer": cached_chat.answer,
                "referenced_books": book_data,
                "cached": True # Lets the frontend know it was served from DB
            })

        # 1. Get answer from RAG pipeline if not cached
        result = query_rag_system(question)
        source_titles = result.get('sources', [])
        
        # 2. Fetch full book details for those sources
        referenced_books = Book.objects.filter(title__in=source_titles)
        book_data = BookSerializer(referenced_books, many=True).data
        
        # 3. Save to Chat History for future caching
        ChatHistory.objects.create(
            question=question,
            answer=result['answer'],
            sources=json.dumps(source_titles)
        )
        
        # 4. Return the answer PLUS the full book metadata for the UI
        return Response({
            "answer": result['answer'],
            "referenced_books": book_data,
            "cached": False
        })