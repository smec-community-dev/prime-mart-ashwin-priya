from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import User
from .models import Seller

@receiver(post_save, sender=User)
def create_or_update_seller(sender, instance, created, **kwargs):
    # Only create seller for seller-role users
    if instance.role == "seller":
        # get_or_create prevents duplicate seller entries
        seller, _ = Seller.objects.get_or_create(
            user=instance,
            defaults={
                "name": instance.first_name or instance.username,
                "phone": "",
                "address": ""
            }
        )