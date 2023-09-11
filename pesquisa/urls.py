from django.urls import path
from . import views

urlpatterns = [
    path('ces/', views.pesquisa_passo_um, name='pesquisa_passo_um'),
    path('ces/comentario', views.pesquisa_passo_dois, name='pesquisa_passo_dois'),
    path('ces/obrigado', views.pesquisa_passo_tres, name='pesquisa_passo_tres'),
    path('api/pesquisas/', views.PesquisasView.as_view(), name='pesquisas'),
]
