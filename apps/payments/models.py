from django.db import models
from apps.orders.models import Order

class PaymentMethod(models.TextChoices):
    ZARINPAL = 'ZP', 'ZarinPal'
    PAYPAL = 'PP', 'PayPal'
    BITCOIN = 'TON', 'Toncoin'
    INPLACEPAYMENT = 'IP', 'InPlacePayment'

# Create your models here.
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=3, choices=PaymentMethod.choices)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id} via {self.get_method_display()}"