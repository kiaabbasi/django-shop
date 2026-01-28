from django.views.generic import ListView,View,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Wallet
from django.shortcuts import get_object_or_404
from apps.payments.models import Payment,PaymentMethod,BalanceType
from apps.payments.signals import payment_successful
from apps.payments.views import get_redirect_url_for_payment
from django.contrib import messages
from django.shortcuts import redirect
from django.db import transaction
from .forms import WalletChargeForm
from apps.orders.models import Order,OrderType

class ShowWallets(LoginRequiredMixin, ListView):
    model = Wallet
    context_object_name = "wallets"
    template_name = "wallet/user_wallets.html"

    def get_queryset(self):
        user = self.request.user
        wallets=[]
        for b in BalanceType:
            wallets.append(get_or_create_wallet(user,b))
        
        return wallets

class PayWithWallet(LoginRequiredMixin,View):
    def get(self,request,payment_id):
        payment = get_object_or_404(
            Payment,id=payment_id,
            method = PaymentMethod.WALLET,)
        if payment.order.user != request.user:
            return "403 frim walet view.py 30"
        
        wallet= get_or_create_wallet(request.user,payment.balance_type)
        
        if payment.successful == False and  wallet.balance >= payment.amount:
            with transaction.atomic():
                wallet.balance -= payment.amount
                wallet.save(update_fields=["balance"])
                payment.successful = True
                payment_successful.send(sender=self, payment=payment)
                payment.save(update_fields=["successful"])
                
            messages.success(request,"successful payment")
            
        else:
            messages.error(request,"Insufficient balance in your wallet.")
        
        
        return redirect("orders:show_all_user_order")  



class ChargWalletRequest(LoginRequiredMixin,FormView):
    form_class = WalletChargeForm
    template_name = "wallet/wallet_charge_form.html"
    #success_url="" go to this payment
    def form_valid(self, form):
        amount = form.cleaned_data["amount"]
        balance_type= form.cleaned_data["balance_type"]
        pay_m=form.cleaned_data["payment_method"]

        #Create order
        order= Order.objects.create(
            user=self.request.user,
            order_type=OrderType.WALLET
            )

        #Create payment
        pay= Payment.objects.create(
            order=order,
            method=pay_m,
            amount=amount,
            balance_type=balance_type
            )
        

        self.success_url = get_redirect_url_for_payment(payment_method=pay_m,payment_id= pay.id)

        return super().form_valid(form)
    


def get_or_create_wallet(user,balanse_type:BalanceType):
    wallet,created = Wallet.objects.get_or_create(
        user = user,
        balance_type = balanse_type,

    )
    return wallet