from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200, null=True, blank=True)
    rating = models.CharField(max_length=50, null=True, blank=True)
    reviews = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    url = models.URLField(max_length=500)
    genre = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    sentiment = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ChatHistory(models.Model):
    question = models.TextField()
    answer = models.TextField()
    sources = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)