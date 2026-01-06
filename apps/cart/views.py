from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.products.models import Product
from .models import Cart, CartItem


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
        return redirect("products:product_detail", pk=product_id)
