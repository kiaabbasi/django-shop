from apps.TonCoin.signals import ton_payment_confirmed
from django.dispatch import receiver,Signal
from .models import Payment,PaymentMethod

payment_successful = Signal()


# TON Payment confirmed signal handler
@receiver(ton_payment_confirmed)
def handle_ton_payment_confirmed(sender, request, transaction, **kwargs):
    payment:Payment = request.payment
    payment.method = PaymentMethod.objects.get(code='TON')
    payment.successful = True
    payment.save()



    payment_successful.send(sender=Payment, payment=payment)
