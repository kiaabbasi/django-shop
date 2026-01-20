from django.dispatch import receiver,Signal
from apps.payments.signals import payment_successful
from .models import Order,OrderStatus
import logging


order_status_changed = Signal()


@receiver(payment_successful)
def handle_order_payment(sender, payment, **kwargs):
    try:
        order = Order.objects.get(payment=payment)
        order.status = OrderStatus.PROCESSING
        
        order.save()
    except Order.DoesNotExist:
        logging.error(f"⚠️ No order found for payment {payment.id}")



@receiver(order_status_changed)
def handle_order_status_change(sender, order, old_status, new_status, **kwargs):
    print(f"🔄 Order {order.id} changed from {old_status} → {new_status} this notif come from orders/signal.py")

    #TODO send notification to user about status change