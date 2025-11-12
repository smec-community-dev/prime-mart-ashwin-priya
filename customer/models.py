from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# -----------------------------
# Customer
# -----------------------------
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.user.username


# -----------------------------
# Cart
# -----------------------------
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('seller.Product', on_delete=models.CASCADE, related_name='cart_entries')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.customer.user.username} - {self.product.name} x {self.quantity}"


# -----------------------------
# Wishlist
# -----------------------------
class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey('seller.Product', on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.customer.user.username} - {self.product.name}"


# -----------------------------
# Search History
# -----------------------------
class SearchHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='search_history')
    search_text = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.customer.user.username} searched '{self.search_text}'"


# -----------------------------
# Orders
# -----------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('out', 'Out for Delivery'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Order #{self.id} - {self.customer.user.username}"


# -----------------------------
# Order Item
# -----------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('seller.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.product.name} x {self.quantity}"



# -----------------------------
# Review
# -----------------------------
class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey('seller.Product', on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()
    rating_value = models.PositiveSmallIntegerField()
    review_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.customer.user.username} - {self.product.name}"


# -----------------------------
# Review Image
# -----------------------------
class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Review #{self.review.id} Image"