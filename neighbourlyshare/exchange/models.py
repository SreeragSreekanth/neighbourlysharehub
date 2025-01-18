from django.db import models
from userauth.models import Register
from itemlisting.models import Item

class ExchangeRequest(models.Model):
    requested_item = models.ForeignKey(Item, related_name="requested_exchanges", on_delete=models.CASCADE)
    offered_item = models.ForeignKey(Item, related_name="offered_exchanges", on_delete=models.CASCADE)
    offered_by = models.ForeignKey(Register, related_name="exchange_requests", on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)  # Field to store the acceptance date

    def __str__(self):
        return f"{self.offered_by.username} offers {self.offered_item.title} for {self.requested_item.title}"
