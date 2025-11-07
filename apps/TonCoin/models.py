from django.db import models
from apps.payments.models import Payment


class TonTransaction(models.Model):
    tx_hash = models.CharField(max_length=255, unique=True)  
    message = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    sender_address= models.CharField(max_length=255,null=True)
    receiver_address = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'TonTransaction {self.tx_hash} ({self.amount} TON)'


class TonPaymentRequest(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='ton_payment_request')
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    address = models.ForeignKey('Wallet_admin', on_delete=models.CASCADE, related_name='wallet')
    message = models.CharField(max_length=255,unique=True)  # unique message to identify the payment
    created_at = models.DateTimeField(auto_now_add=True)
    mached_transaction = models.ForeignKey(TonTransaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='matched_request')
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'Request for {self.amount} TON to {self.address}'


class Wallet_admin(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, unique=True)
    details = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.address}'