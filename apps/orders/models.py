from django.db import models
from django.conf import settings


class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PROCESSING = 'PROCESSING', 'Processing'
    SHIPPED = 'SHIPPED', 'Shipped'
    DELIVERED = 'DELIVERED', 'Delivered'
    CANCELED = 'CANCELED', 'Canceled'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} - {self.user}"
    
    def save(self, *args, **kwargs):
        # وضعیت قبلی را پیدا کن
        if self.pk:
            old_status = Order.objects.get(pk=self.pk).status
        else:
            old_status = None

        super().save(*args, **kwargs)
        from .signals import order_status_changed
        # اگر تغییر کرده بود، سیگنال بفرست
        if old_status and old_status != self.status:
            order_status_changed.send(
                sender=self.__class__,
                order=self,
                old_status=old_status,
                new_status=self.status,
            )
