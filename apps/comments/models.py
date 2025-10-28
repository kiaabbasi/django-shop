from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product

User = get_user_model()

class ratingChoices(models.IntegerChoices):
    ONE = 1, '1 Star'
    TWO = 2, '2 Stars'
    THREE = 3, '3 Stars'
    FOUR = 4, '4 Stars'
    FIVE = 5, '5 Stars'
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    on_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    rate = models.IntegerField(choices=ratingChoices.choices, null=True, blank=True)
    
    def __str__(self):
        return self.content[:20] + "..." if len(self.content) > 20 else ""  # Return first 20 characters of the comment
    
