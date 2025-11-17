from django.db import models
from core.models import Category, User

# -----------------------------
# Seller
# -----------------------------
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'seller'})
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name


# -----------------------------
# Product
# -----------------------------
class Product(models.Model):
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,       # allow NULL temporarily
        blank=True       # optional for forms
    )
    name = models.CharField(max_length=255,default='DefaultProduct')
    # other fields...
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name


# -----------------------------
# Product Image
# -----------------------------
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_file=models.ImageField(upload_to='products/',null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.product.name} Image"