from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.search_books),
    path('posts/', views.search_posts)
]
