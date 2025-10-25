from django.db import models
from django.contrib.auth.models import User
from apps.products.models import Product

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    on_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    def __str__(self):
        return self.content[:20] + "..." if len(self.content) > 20 else ""  # Return first 20 characters of the comment