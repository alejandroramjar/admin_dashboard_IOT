from django.urls import path

from backend.accounts import views

urlpatterns = [
    path('register/', views.RegistroUsuario, name='register'),
]
