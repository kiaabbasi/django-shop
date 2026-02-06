from django.shortcuts import render
from django.views.generic import ListView ,DetailView
from .models import Product
from apps.comments.forms import CommentForm
from django.db.models import Prefetch
from apps.comments.models import Comment

class ProductsView(ListView):
    template_name = 'products/index.html'
    model = Product
    
    context_object_name = "products"      # optional, پیش‌فرض: object_list
    paginate_by = 10  

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
    

def product_search(request):
    query = request.GET.get('q', '')  # گرفتن متن جستجو از URL
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()  # اگر خالی بود، همه محصولات

    context = {
        "products": products,
        "query": query,
    }
    return render(request, "products/product_list.html", context)
