# property/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Property, Developer
from blogs.models import Post
from shop.models import Product
from bookings.models import Apartment
from listings.utils.indexnow import notify_indexnow


@receiver(post_save, sender=Property)
def submit_property_to_indexnow(sender, instance, created, **kwargs):
    if instance.is_active:
        url = f'https://nestovaproperty.com{instance.get_absolute_url()}'
        notify_indexnow(url)


@receiver(post_save, sender=Developer)
def submit_developer_to_indexnow(sender, instance, created, **kwargs):
    if instance.is_active:
        url = f'https://nestovaproperty.com{instance.get_absolute_url()}'
        notify_indexnow(url)


@receiver(post_save, sender=Post)
def submit_post_to_indexnow(sender, instance, created, **kwargs):
    if instance.status == 'published':
        url = f'https://nestovaproperty.com{instance.get_absolute_url()}'
        notify_indexnow(url)


@receiver(post_save, sender=Product)
def submit_product_to_indexnow(sender, instance, created, **kwargs):
    if instance.is_available:
        url = f'https://nestovaproperty.com{instance.get_absolute_url()}'
        notify_indexnow(url)


@receiver(post_save, sender=Apartment)
def submit_apartment_to_indexnow(sender, instance, created, **kwargs):
    if instance.status == 'available':
        url = f'https://nestovaproperty.com/bookings/apartment/{instance.slug}/'
        notify_indexnow(url)
