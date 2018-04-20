
from django.urls import path

from . import views

urlpatterns = [
    # ex: /julopedia/
    path('', views.index, name='index'),
    
    path('node/<path:node_path_str>/', views.node, name='node'),
    
    
    #path('guide/<path:guide_path>/', views.guide, name='guide'),
    
    path('create/<str:author_name>/', views.createData, name='createData'),
]
