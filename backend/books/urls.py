from django.urls import path
from .views import (
    BookListView, 
    BookDetailView, 
    RAGQueryView, 
    RecommendView
)

urlpatterns = [
    # Requirement: GET API - Lists all uploaded books
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Requirement: GET API - Retrieves all details about each book
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Requirement: GET API - Recommends related books (Similarity Search)
    path('books/<int:pk>/recommend/', RecommendView.as_view(), name='book-recommend'),
    
    # Requirement: POST API - Asking questions (RAG query endpoint)
    path('chat/', RAGQueryView.as_view(), name='rag-query'),
]