from django.urls import path
from . import views

urlpatterns = [
    path('request/<int:payment_id>', views.send_request, name='request'),
    path('verify/<int:payment_id>', views.verify , name='verify'),
    
]