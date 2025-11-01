from django.db import models
from apps.payments.models import Payment


class TonTransaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='ton_transactions')
    tx_hash = models.CharField(max_length=255, unique=True)  # نام فیلد واضح‌تر شد
    message = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'TonTransaction {self.tx_hash} ({self.amount} TON)'


class TonPaymentRequest(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='ton_payment_request')
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    address = models.CharField(max_length=255)  # آدرس ولت شما که کاربر بهش پول می‌فرسته
    message = models.CharField(max_length=255, blank=True, null=True)  # مثل عدد شناسه کاربر
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Request for {self.amount} TON to {self.address}'
