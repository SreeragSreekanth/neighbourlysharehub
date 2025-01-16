from django.db import models

class Category(models.Model):
    """Model to represent item categories."""
    name = models.CharField(max_length=100, unique=True)  # Category name

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    


