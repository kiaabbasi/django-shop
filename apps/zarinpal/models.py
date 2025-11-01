from django.db import models
from apps.payments.models import Payment
# Create your models here.

class Bank_Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True) 
    payment_on  = models.ForeignKey(Payment, on_delete=models.RESTRICT)
    paymentid=models.CharField(max_length=256)

