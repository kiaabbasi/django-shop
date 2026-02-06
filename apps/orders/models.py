from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product

class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PROCESSING = 'PROCESSING', 'Processing'
    SHIPPED = 'SHIPPED', 'Shipped'
    DELIVERED = 'DELIVERED', 'Delivered'
    CANCELED = 'CANCELED', 'Canceled'

class OrderItem(models.Model):
    on_order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) 
    added_at = models.DateTimeField(auto_now_add=True)

class OrderType(models.TextChoices):
    Buy = "BUY"
    WALLET = "WALLET"


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order_type = models.CharField(max_length=10,choices=OrderType.choices,default=OrderType.Buy)
    order_date = models.DateTimeField(auto_now_add=True)
    update_at  = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    def __str__(self):
        return f"Order #{self.id} - {self.user}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Order.objects.get(pk=self.pk).status
        else:
            old_status = None

        super().save(*args, **kwargs)
        from .signals import order_status_changed
        
        if old_status and old_status != self.status:
            order_status_changed.send(
                sender=self.__class__,
                order=self,
                old_status=old_status,
                new_status=self.status,
            )
