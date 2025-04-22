from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('advisory/create/', views.create_advisory, name='create_advisory'),
    path('advisory/<int:pk>/edit/', views.edit_advisory, name='edit_advisory'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]