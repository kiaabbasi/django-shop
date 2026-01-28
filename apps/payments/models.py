from django.db import models
from apps.orders.models import Order

class PaymentMethod(models.TextChoices):
    ZARINPAL = 'ZP', 'ZarinPal'
    #PAYPAL = 'PP', 'PayPal'
    TonCoin = 'TON', 'Toncoin'
    INPLACEPAYMENT = 'IP', 'InPlacePayment'
    WALLET = 'WAL', 'InternalWallet'

class BalanceType(models.TextChoices):
        DOLER = 'DOLER', 'Doler'
        TONCOIN = 'TONCOIN', 'Toncoin'
        RIAL = 'RIAL', 'Rial'


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=3, choices=PaymentMethod.choices)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    balance_type = models.CharField(max_length=10, choices=BalanceType.choices,default=BalanceType.RIAL)
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id} via {self.get_method_display()}"