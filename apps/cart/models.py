from django.db import models
from apps.products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)    
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discription = models.TextField(null=True, blank=True)
    on_cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name} for {self.on_cart.user.username}"
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Cart of {self.user.username}"
