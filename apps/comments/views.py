from django.shortcuts import render
from django.views.generic import FormView,DeleteView
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404,redirect
from apps.products.models import Product
from .models import Comment
from django.contrib import messages

class AddComment(LoginRequiredMixin,FormView):
    form_class = CommentForm
    

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs["pk"])
        reply_id = self.request.POST.get("reply_to")
        
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.on_product = product

        if reply_id:
            comment.reply_to = Comment.objects.get(pk=reply_id)

        comment.save()
        messages.success(self.request, "Comment added successfully.")
        return redirect(product.get_absolute_url())


