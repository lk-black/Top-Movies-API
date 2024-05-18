"""
Rotas de url para o users API.
"""
from django.urls import path
from users import views


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
