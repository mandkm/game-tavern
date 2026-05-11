from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_library, name='game_list'),
    path('search/', views.game_search, name='game_search'),
    path('<int:game_id>/toggle/', views.toggle_owned, name='toggle_owned'),
]