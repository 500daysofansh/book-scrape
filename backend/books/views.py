from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from .rag_pipeline import query_rag_system

class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookDetailView(APIView):
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            return Response(BookSerializer(book).data)
        except Book.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

class RAGQueryView(APIView):
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({"error": "No question provided"}, status=400)
        
        # This calls your rag_pipeline.py logic
        result = query_rag_system(question)
        return Response(result)