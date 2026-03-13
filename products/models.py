from django.db import models

# Create your models here.

# class Unit(models.Model):
#     name = models.CharField(max_length=50)
#     code = models.CharField(max_length=10, unique=True)

#     def __str__(self):
#         return  f"{self.name} ({self.code})"


class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, null=True)
    description = models.TextField(blank=True)
    # unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='products')

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name