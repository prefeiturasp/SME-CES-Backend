from django.urls import path
from . import views

urlpatterns = [
    path('api/usuarios/', views.UsuariosView.as_view({'post': 'create'}), name='usuarios'),
]
