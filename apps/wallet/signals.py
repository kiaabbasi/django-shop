from apps.payments.signals import payment_successful
from apps.payments.models import Payment
from apps.orders.models import OrderType
from .views import get_or_create_wallet
from django.dispatch import receiver
from django.db import transaction
#This code handel charg on wallets
@receiver(payment_successful)
def handel_wallet_sharg(sender, payment, **kwargs):
    if payment.order.order_type == OrderType.WALLET:
        w= get_or_create_wallet(payment.order.user,payment.balance_type)
        with transaction.atomic():
            w.balance += payment.amount
            w.save(update_fields="balance")
            
        