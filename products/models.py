from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return  f"{self.name} ({self.code})"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    branch = models.ForeignKey(branch, on_delete=models.PROTECT, related_name='products', default=1)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='products', default=1)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
