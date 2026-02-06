from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email","phone_number"]

        widgets = {
            "username": forms.TextInput(attrs={"class": "border rounded p-2 w-full"}),
            "first_name": forms.TextInput(attrs={"class": "border rounded p-2 w-full"}),
            "last_name": forms.TextInput(attrs={"class": "border rounded p-2 w-full"}),
            "email": forms.EmailInput(attrs={"class": "border rounded p-2 w-full"}),
            "phone_number" :forms.TextInput(attrs={"class": "border rounded p-2 w-full"}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "border rounded p-2 w-full"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "border rounded p-2 w-full"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "border rounded p-2 w-full"}))
