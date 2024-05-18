"""
Rotas de url para movies API. 
"""
from django.urls import path
from .views import ListMoviesView

urlpatterns = [
    path('', ListMoviesView.as_view()),
]