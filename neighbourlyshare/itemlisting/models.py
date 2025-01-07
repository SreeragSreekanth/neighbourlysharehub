from django.db import models
from userauth.models import Register

class ItemImage(models.Model):
    """Model to represent an image for a specific item."""
    image = models.ImageField(upload_to="products/items/")  # Store the image in the specified folder

    def __str__(self):
        return f"Image {self.id} for item"

class Item(models.Model):
    """Model to represent an item listing."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='items', null=True, blank=True)

    # Change from ImageField to ManyToManyField to allow multiple images
    images = models.ManyToManyField(ItemImage, related_name='items', blank=True)

    def __str__(self):
        return self.title
