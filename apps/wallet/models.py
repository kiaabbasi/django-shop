from django.db import models
from django.contrib.auth import get_user_model
from apps.payments.models import BalanceType,Payment
User = get_user_model()

"""
class WalletTransaction(models.Model):
    TRANSACTION_TYPE = (
        ("CHARGE","Charge"),
        ("SPEND","Spend"))

    wallet = models.ForeignKey('Wallet',on_delete=models.CASCADE,related_name="transactions")
    amount = models.DecimalField(max_digits=30, decimal_places=6, default=0.00)
    balance_type = models.CharField(max_length=20,choices=BalanceType.choices)
    tran_type = models.CharField(max_length=20,choices=TRANSACTION_TYPE)
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.OneToOneField(Payment,on_delete=models.CASCADE)
     """

class Wallet(models.Model):   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')  # User can have multiple wallets
    balance = models.DecimalField(max_digits=30, decimal_places=6, default=0.00)
    balance_type = models.CharField(
        max_length=20,
        choices=BalanceType.choices,
        default=BalanceType.RIAL
    )
    class Meta:
        unique_together = ('user','balance_type')
    def __str__(self):
        return f"{self.user.username}'s Wallet ({self.balance_type}) {self.balance:.2f}"
