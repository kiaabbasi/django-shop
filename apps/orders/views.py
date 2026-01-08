from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
from apps.cart.models import Cart
from django.utils.decorators import method_decorator
from .models import Order,OrderItem
from django.db import transaction
from django.contrib import messages
from django.views.generic import DetailView,ListView

@method_decorator(login_required, name='dispatch')
class CreateOrder(View):
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)

        if not cart.items.exists():
            messages.error(request, "سبد خرید خالی است ❌")
            return redirect("cart:show_cart")

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    on_order=order,
                    product=item.product,
                    quantity = item.quantity
                )

            # خالی کردن سبد خرید
            cart.items.all().delete()

        messages.success(request, "سفارش با موفقیت ثبت شد ✅")
        return redirect("orders:order_detail", pk=order.id)

@method_decorator(login_required, name='dispatch')
class ShowOrder(DetailView):
    model = Order
    template_name = 'orders/show order.html'
    context_object_name = 'order'
    
    
    def get_object(self):
        return get_object_or_404(
            Order,
            pk=self.kwargs["pk"],
            user=self.request.user
        )
       


@method_decorator(login_required, name='dispatch')
class ShowOrders(ListView):
    model = Order
    template_name = 'orders/show orders.html'
    context_object_name = 'orders'
    paginate_by = 0
    
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-order_date')
