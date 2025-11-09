from .views import LoginView,SendOTPView
from django.urls import path
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('sendOTP/', SendOTPView.as_view(), name='send_otp'),
]