"""
Rotas de url para movies API. 
"""
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('movies/list', views.PersonalMovieListView, basename='personal-list-movies')


urlpatterns = [
    path('movies/', views.ListMoviesView.as_view(), name='movies-list'),
    path('movies/details/', views.DetailMovieView.as_view(), name='movie-details'),
    path('movies/add/', views.AddMovieView.as_view(), name='add-movie'),
    path('', include(router.urls)),
]
