from django.urls import path
from . import views

urlpatterns = [
    path('ces/', views.atribuir_nota_view, name='atribuir_nota'),
    path('ces/comentario', views.atribuir_comentario_view, name='atribuir_comentario'),
    path('ces/obrigado', views.agradecimento_view, name='agradecimento'),
    path('api/pesquisas/', views.PesquisasView.as_view(), name='pesquisas'),
]
