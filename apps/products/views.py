from django.shortcuts import render
from django.views.generic import ListView ,DetailView
from .models import Product
from apps.comments.forms import CommentForm
from django.db.models import Prefetch
from apps.comments.models import Comment

class ProductsView(ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'
    paginate_by = 10  # اختیاری، برای pagination

    def get_queryset(self):
        """
        اگر پارامتر ?q= در URL باشد → جستجو
        در غیر این صورت → همه محصولات
        """
        query = self.request.GET.get('q', '')
        qs = Product.objects.all()
        if query:
            qs = qs.filter(name__icontains=query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # تا فیلد جستجو پر شود
        return context

class ProductView(DetailView):
    model = Product
    template_name = 'products/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        comments = Comment.objects.filter(
            on_product=product,
            reply_to__isnull=True
        ).prefetch_related(
            Prefetch(
                "replies",
                queryset=Comment.objects.select_related("user").prefetch_related("replies")
            )
        ).select_related("user")

        context["comments"] = comments
        context["form"] = CommentForm()
        
        return context
    

