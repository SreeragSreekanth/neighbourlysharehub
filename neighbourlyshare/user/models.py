from django.db import models
from userauth.models import Register
from itemlisting.models import Item
# Create your models here.

class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="ratings")
    reviewer = models.ForeignKey(Register, on_delete=models.CASCADE, related_name="reviews_given")
    reviewee = models.ForeignKey(Register, on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    review_text = models.TextField(blank=True, null=True)  # Optional review text
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review from {self.reviewer.username} to {self.reviewee.username} on {self.item.title}"

    class Meta:
        unique_together = ['item', 'reviewer']

