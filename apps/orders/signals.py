from django.dispatch import receiver
from apps.payments.signals import payment_successful
from .models import Order,OrderStatus
import logging
@receiver(payment_successful)
def handle_order_payment(sender, payment, **kwargs):
    try:
        order = Order.objects.get(payment=payment)
        order.status = OrderStatus.PROCESSING
        
        order.save()
    except Order.DoesNotExist:
        logging.error(f"⚠️ No order found for payment {payment.id}")
