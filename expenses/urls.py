from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.expense_history, name='history'),
    path('edit/<int:pk>/', views.expense_edit, name='expense_edit'),
    path('delete/<int:pk>/', views.expense_delete, name='expense_delete'),
    path('day/<str:date_str>/', views.daily_detail, name='daily_detail'),
]