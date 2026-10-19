# property/management/commands/submit_indexnow.py

from django.core.management.base import BaseCommand
from property.models import Property, Developer
from listings.utils.indexnow import notify_indexnow


class Command(BaseCommand):
    help = 'Submit all active properties and developers to IndexNow'

    def handle(self, *args, **kwargs):

        # ── Properties ─────────────────────────────────────────────────────
        property_urls = [
            f'https://nestovaproperty.com{p.get_absolute_url()}'
            for p in Property.objects.filter(is_active=True)
        ]

        # ── Developers ─────────────────────────────────────────────────────
        developer_urls = [
            f'https://nestovaproperty.com{d.get_absolute_url()}'
            for d in Developer.objects.filter(is_active=True)
        ]

        all_urls = property_urls + developer_urls

        if not all_urls:
            self.stdout.write('No active records found.')
            return

        # Submit in chunks of 100
        chunk_size = 100
        for i in range(0, len(all_urls), chunk_size):
            chunk = all_urls[i:i + chunk_size]
            status = notify_indexnow(chunk)
            self.stdout.write(f'Submitted {len(chunk)} URLs — Status: {status}')

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Done!'
            f'\n   Properties submitted : {len(property_urls)}'
            f'\n   Developers submitted : {len(developer_urls)}'
            f'\n   Total                : {len(all_urls)}'
        ))