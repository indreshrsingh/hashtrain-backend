from django.urls import path
from . import views


urlpatterns = [
    path('trainings/', views.training_list, name='training_list'),
    path('trainings/<int:pk>/', views.training_detail, name='training_detail'),
]
