from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book, ChatHistory
from .serializers import BookSerializer
from .rag_pipeline import query_rag_system, collection
import json

# 1. Dashboard: List all books
class BookListView(APIView):
    """
    Requirement: GET API to list all uploaded books.
    """
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

# 2. Detail Page: Get a single book's details
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

# 3. Recommendations: "If you like X, you'll like Y"
class RecommendView(APIView):
    """
    Requirement: AI-based recommendation logic using Vector Similarity.
    """
    def get(self, request, pk):
        try:
            target_book = Book.objects.get(pk=pk)
            
            # Query ChromaDB for 3 similar books
            results = collection.query(
                query_texts=[target_book.description],
                n_results=4 
            )
            
            # Filter out the current book's ID and fetch others from MySQL
            similar_ids = [id for id in results['ids'][0] if id != str(pk)]
            recommended = Book.objects.filter(id__in=similar_ids)
            
            serializer = BookSerializer(recommended, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 4. RAG Chat: Ask questions about the documents
class RAGQueryView(APIView):
    """
    Requirement: POST API for RAG-based Q&A.
    """
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({"error": "No question provided"}, status=400)
        
        # Get answer from RAG pipeline
        result = query_rag_system(question)
        
        # Bonus Requirement: Save to Chat History
        ChatHistory.objects.create(
            question=question,
            answer=result['answer'],
            sources=json.dumps(result['sources'])
        )
        
        return Response(result)