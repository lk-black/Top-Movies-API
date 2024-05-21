"""
Rotas de url para movies API. 
"""
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('movies', views.MoviesAPIView)

app_name = 'movies'


urlpatterns = [
    path('', include(router.urls)),
]
