from apps.payments.models import Payment
from apps.wallet.views import get_or_create_wallet
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
from apps.cart.models import Cart
from django.utils.decorators import method_decorator
from .models import Order,OrderItem,OrderStatus
from django.db import transaction
from django.contrib import messages
from django.views.generic import DetailView,ListView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden

class CreateOrder(LoginRequiredMixin,View):
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


class ShowOrder(LoginRequiredMixin,DetailView):
    model = Order
    template_name = 'orders/show order.html'
    context_object_name = 'order'
    
    
    def get_object(self):
        return get_object_or_404(
            Order,
            pk=self.kwargs["pk"],
            user=self.request.user
        )
       


class ShowOrders(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders/show orders.html'
    context_object_name = 'orders'
    paginate_by = 0
    
    
    

class CanselOrder(LoginRequiredMixin,UpdateView):
    model = Order
    fields =[]
    success_url =  reverse_lazy("orders:show_all_user_order")

    template_name = "orders/cansel order.html"

    def get_object(self):
        order = get_object_or_404(Order,pk=self.kwargs["pk"])

        if order.user != self.request.user:
            raise HttpResponseForbidden("You are not allowed to cansel this order")
        
        if order.status in [OrderStatus.PENDING,OrderStatus.PROCESSING]:
            return order
        
        else :
            return None
        

    def form_valid(self, form):
        order:Order = form.instance
        with transaction.atomic():
            if order.status == OrderStatus.PROCESSING : # or some ways user payed
                p:Payment= order.payment#REfund
                price= p.amount
                type_p = p.balance_type
                user = order.user
                w=get_or_create_wallet(user,type_p)
                w.balance+=price
                w.save(update_fields=["balance"])

            order.status = OrderStatus.CANCELED
            order.save(update_fields=["status"])
            messages.success(self.request,"Order canseled")
        return super().form_valid(form)
    