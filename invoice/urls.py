from django.urls import path
from . import views

urlpatterns = [
    path('generate-invoice/', views.generate_invoice, name='generate_invoice'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),  # Adjust the URL pattern as needed
    # Add other URL patterns as necessary
]
