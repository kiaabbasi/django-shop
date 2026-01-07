from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import  DetailView
from apps.products.models import Product
from .models import Cart, CartItem


@method_decorator(login_required, name='dispatch')
class ShowCart(DetailView):
    model = Cart
    template_name = 'cart/show cart.html'
    context_object_name = 'cart'
    
    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        quantity = int(request.POST.get("quantity", 1))

        cart, created = Cart.objects.get_or_create(user=request.user)

        item, item_created = CartItem.objects.get_or_create(
            on_cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        # اگر قبلاً وجود داشت → فقط quantity را زیاد کن
        if not item_created:
            item.quantity += quantity
            item.save()    
        
        messages.success(request, "Product added to cart successfully ✅")
        return redirect(request.META.get("HTTP_REFERER", "/"))

@method_decorator(login_required, name='dispatch')
class DecreaseFromCart(View):
    def post(self, request, product_id):
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, on_cart=cart, product_id=product_id)

        quantity = int(request.POST.get("quantity", 1))
        if item.quantity > quantity :
            item.quantity -=quantity
            item.save()
        else:
            item.delete()
        
        messages.success(request, "Product removed from cart ❌")
        return redirect(request.META.get("HTTP_REFERER", "/"))
    




@method_decorator(login_required, name='dispatch')
class CheckOut(View):
    def post(self, request, product_id):
        cart = get_object_or_404(Cart, user=request.user)
        messages.success(request, "Product removed from cart ❌")
        return redirect(request.META.get("HTTP_REFERER", "/"))