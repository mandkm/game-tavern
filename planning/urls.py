from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teilnahme/<int:entry_id>/', views.participate, name='participate'),
]
