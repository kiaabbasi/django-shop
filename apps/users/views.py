from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View,UpdateView
from django.http import JsonResponse
from .models import OTPVerification
import random
from kavenegar import KavenegarAPI
from core.settings import SMS_API_KEY
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserUpdateForm,CustomPasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView


User = get_user_model()




class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name)
    

    def post(self, request):
        # Handle login logic here
        otp = request.POST.get('otppassword')
        
        if str(otp)!="" and str(otp) != "None":
            return self.handle_otp(request)
        else:
            return self.handle_password(request)
           
    def handle_otp(self, request):
    
        username = request.POST.get('username')
        otp = request.POST.get('otppassword')
        user = authenticate(request, username=username)
        if user:
            OTP_v= OTPVerification.objects.filter(user=user,otp_code=otp).last()
            if OTP_v and OTP_v.is_valid():
                login(request, user)
                return redirect("products:product_list")
        return render(request, self.template_name, {'message': 'username or password is incorrect'})
    
    def handle_password(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        
        if user :
            login(request,user)
            return redirect("products:product_list")
        return render(request, self.template_name, {'message': 'username or password is incorrect'})

class SendOTPView(View):

    def post(self, request):
        user_info = request.POST.get('user_info')
        user = None
        if '@' in user_info:
            # Assume it's an email
            user = authenticate(request,email=user_info)

        elif user_info.startswith('+') or user_info.isdigit():
            # Assume it's a phone number
            user = authenticate(request,phone_number=user_info)

        else :
            # Assume it's a username
            user = authenticate(request,username=user_info)

        
        if user :
            code = str(random.randint(100_000,999_999))
            OTPVerification.objects.create(user=user,otp_code=code)
            print(code)
            otpa = KavenegarAPI(SMS_API_KEY)
            params = { 'sender' : '2000660110', 'receptor': user.phone_number, 'message' :f'رمز عبور یک بار مصرف شما {code}' }
            response = otpa.sms_send(params)
            return JsonResponse({"message":"OTP Sent"},)
        else :
            return JsonResponse({"message":"Faild To send"},)
        
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial.update({
            "first_name": user.first_name,
            "last_name":  user.last_name,
            "email":      user.email,
            "username":   user.username,
            "phone_number": user.phone_number
        })
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Your profile was updated successfully!")
        return super().form_valid(form)


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "users/change_password.html"
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully!")
        return super().form_valid(form)
