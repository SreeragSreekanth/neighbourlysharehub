from django.db import models
from userauth.models import Register
from category_management.models import Category
from django.db.models import Avg


class Item(models.Model):
    """Model to represent an item listing."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items'
    )
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending',  # Default status is 'pending'
    )

    def __str__(self):
        return self.title
    
    def average_rating(self):
        return self.ratings.aggregate(Avg('rating'))['rating__avg'] or 0

class ItemImage(models.Model):
    """Model to represent an image for a specific item."""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images', null=True)
    image = models.ImageField(upload_to="products/items/", null=True, blank=True)

    def __str__(self):
        return f"Image {self.id} for {self.item.title}"

    def clean(self):
        # Add custom validation if needed
        super().clean()

