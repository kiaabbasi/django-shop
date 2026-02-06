from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "rate"]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Write your comment...",
                    "class": "w-full border rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                }
            ),
            "rate": forms.Select(
                attrs={
                    "class": "mt-3 border rounded p-2 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                }
            ),
        }
