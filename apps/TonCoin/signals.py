from django.db.models.signals import post_save
from django.dispatch import receiver,Signal
from .models import TonTransaction,TonPaymentRequest

ton_payment_confirmed = Signal()

@receiver(post_save, sender=TonTransaction)
def check_ton_transaction_after_create(sender, instance:TonTransaction, created, **kwargs):
    if created:
        req = TonPaymentRequest.objects.filter(message=instance.message, is_completed=False).first()
        if req and instance.amount >= req.amount:
            instance.mached_transaction = req
            req.is_completed = True
            instance.save()

            # Send Signal to the peyment app 
            ton_payment_confirmed.send(sender=TonTransaction, request=req, transaction=instance)
