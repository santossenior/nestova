# property/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Property, Developer
from listings.utils.indexnow import notify_indexnow


@receiver(post_save, sender=Property)
def submit_property_to_indexnow(sender, instance, created, **kwargs):
    if instance.is_active:
        # get_absolute_url() uses reverse('property_detail', slug=...)
        # property app has no prefix in main urls.py → path("", include("property.urls"))
        url = f'https://nestovaproperty.com{instance.get_absolute_url()}'
        notify_indexnow(url)


@receiver(post_save, sender=Developer)
def submit_developer_to_indexnow(sender, instance, created, **kwargs):
    if instance.is_active:
        # get_absolute_url() uses reverse('developer_detail', slug=...)
        url = f'https://nestovaproperty.com{instance.get_absolute_url()}'
        notify_indexnow(url)