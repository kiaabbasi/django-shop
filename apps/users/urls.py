from .views import LoginView,SendOTPView,UserProfileUpdateView,UserPasswordChangeView
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('sendOTP/', SendOTPView.as_view(), name='send_otp'),
    path("logout/",LogoutView.as_view(next_page='products:product_list'),name="logout"),
    path("profile/", UserProfileUpdateView.as_view(), name="profile"),
    path("profile/change-password/", UserPasswordChangeView.as_view(), name="change_password")
]
