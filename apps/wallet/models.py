from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Wallet(models.Model):
    class BalanceType(models.TextChoices):
        DOLER = 'DOLER', 'Doler'
        TONCOIN = 'TONCOIN', 'Toncoin'
        RIAL = 'RIAL', 'Rial'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')  # User can have multiple wallets
    balance = models.DecimalField(max_digits=10, decimal_places=6, default=0.00)
    balance_type = models.CharField(
        max_length=20,
        choices=BalanceType.choices,
        default=BalanceType.RIAL
    )

    def __str__(self):
        return f"{self.user.username}'s Wallet ({self.balance_type})"
