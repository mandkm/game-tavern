from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teilnahme/<int:entry_id>/', views.participate, name='participate'),
    path('termine/', views.entry_list, name='entry_list'),
    path('auswertung/<int:entry_id>/', views.evaluate, name='evaluate'),
    path('erinnerung/<int:entry_id>/', views.send_reminder, name='send_reminder'),
]
