
from django.urls import path

from . import views

urlpatterns = [
    # ex: /julopedia/
    path('', views.index, name='index'),
    # ex: /julopedia/article/biofisica/cinematica/
    path('article/<path:article_path>/', views.article, name='article'),
    path('guide/<path:guide_path>/', views.guide, name='guide'),
    
    path('create/<str:author_name>/', views.createData, name='createData'),
]
