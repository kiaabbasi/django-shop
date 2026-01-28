from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views import View
from .models import Payment,PaymentMethod
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Order
from django.urls import reverse


def get_redirect_url_for_payment(payment_method,payment_id):
    
    
    
    if payment_method == PaymentMethod.TonCoin:
        pass
    elif payment_method == PaymentMethod.ZARINPAL:
        return  reverse("zarinpall:request",args=[payment_id])
    elif payment_method == PaymentMethod.WALLET:
        return reverse("wallet:request",args=[payment_id])
    elif payment_method == PaymentMethod.INPLACEPAYMENT:
        pass





class CreatePayment(LoginRequiredMixin,CreateView):
    model = Payment
    template_name = 'payments/payment_form.html'

    fields = ["method"]
    
    

    def form_valid(self, form):
        payment = form.save(commit=False)
        amount=0
        for i in self.order.items.all():    
            amount += i.quantity* i.product.price
        
        

        payment.order = self.order
        payment.amount = amount
        payment.user = self.request.user
        payment.save()
        self.success_url =get_redirect_url_for_payment(form.cleaned_data['method'],payment.id)

        
        return super().form_valid(form)


    def dispatch(self, request, *args, **kwargs):
        
        self.order = get_object_or_404(
            Order,
            id=kwargs['order_id'],
            user=request.user
        )
        if hasattr(self.order, 'payment'):
            return redirect(get_redirect_url_for_payment(self.order.payment.method,self.order.payment.id))
        return super().dispatch(request, *args, **kwargs)
    