from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# -----------------------------
# Custom User
# -----------------------------
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('offline', 'Offline'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default="seller")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)



# -----------------------------
# Category
# -----------------------------

class Category(models.Model):
    name = models.CharField(max_length=255, default='DefaultCategory')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name


