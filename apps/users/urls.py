from .views import LoginView,SendOTPView
from django.urls import path
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('sendOTP/', SendOTPView.as_view(), name='send_otp'),
    path("logout/",LogoutView.as_view(next_page='products:product_list'),name="logout")
]