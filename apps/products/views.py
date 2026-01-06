from django.shortcuts import render
from django.views.generic import ListView ,DetailView
from .models import Product

class ProductsView(ListView):
    template_name = 'products/index.html'
    model = Product
    
    context_object_name = "products"      # optional, پیش‌فرض: object_list
    paginate_by = 10  

class ProductView(DetailView):
    model = Product
    template_name = 'products/product.html'
    context_object_name = 'product'
    
