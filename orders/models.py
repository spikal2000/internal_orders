from django.db import models
from django.conf import settings
from products.models import Product, branch


# Create your models here.

class InternalOrder(models.Model):
    STATUS_CHOICES = [
        ('unread', 'Αδιάβαστο'),
        ('read', 'Διαβάστηκε'),
        ('in_progress', 'Σε εξέλιξη'),
        ('ready', 'Έτοιμο'),
        ('delivered', 'Παραδόθηκε'),
    ]

    branch = models.ForeignKey(branch, on_delete=models.CASCADE, related_name='internal_orders')
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='internal_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unread')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.branch_id.name} - {self.get_status_display()}"
    


class InternalOrderItem(models.Model):
    order = models.ForeignKey(
        InternalOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


