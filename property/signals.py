# property/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Property, Developer
from listings.utils.indexnow import notify_indexnow


# ── Property Signal ────────────────────────────────────────────────────────

@receiver(post_save, sender=Property)
def submit_property_to_indexnow(sender, instance, created, **kwargs):
    """
    Fires every time a Property is saved.
    Only submits if the property is active/published.
    """
    if instance.is_active:
        # Uses the exact get_absolute_url() already in your model
        url = f'https://nestovaproperty.com{instance.get_absolute_url()}'
        notify_indexnow(url)


# ── Developer Signal ───────────────────────────────────────────────────────

@receiver(post_save, sender=Developer)
def submit_developer_to_indexnow(sender, instance, created, **kwargs):
    """
    Fires every time a Developer profile is saved.
    Only submits if the developer is active.
    """
    if instance.is_active:
        # Uses the exact get_absolute_url() already in your model
        url = f'https://nestovaproperty.com{instance.get_absolute_url()}'
        notify_indexnow(url)