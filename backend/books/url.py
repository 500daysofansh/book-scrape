from django.urls import path
from .views import BookListView, BookDetailView, RAGQueryView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('chat/', RAGQueryView.as_view(), name='rag-query'),
]