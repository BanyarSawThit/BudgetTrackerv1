from django.db import models
from django.utils import timezone


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('meal', 'Meal'),
        ('drink', 'Drink'),
        ('snacks', 'Snacks & Fun'),
        ('grocery', 'Grocery'),
        ('health', 'Health & Medication'),
        ('utility', 'Utility'),
        ('cosmetic', 'Cosmetic'),
        ('wear', 'Wear'),
    ]

    name  = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=Category.CATEGORY_CHOICES, default='meal')
    description = models.CharField(max_length=200, blank=True, default='')
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.get_category_display()} - {self.amount}"


class Income(models.Model):
    """Income tracking"""
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, default='')
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.source}: {self.amount}"

    class Meta:
        ordering = ['-date', '-created_at']