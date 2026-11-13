"""Idempotent starter data so the live site and API have something to show."""
from django.core.management.base import BaseCommand

from inventory.models import Manufacturer

MANUFACTURERS = [
    ("Toyota", "Japan", 1937),
    ("Ford", "United States", 1903),
    ("Volkswagen", "Germany", 1937),
    ("Honda", "Japan", 1948),
    ("Mercedes-Benz", "Germany", 1926),
]


class Command(BaseCommand):
    help = "Create demo manufacturers (safe to run repeatedly)."

    def handle(self, *args, **options):
        created = 0
        for name, country, founded in MANUFACTURERS:
            _, was_created = Manufacturer.objects.get_or_create(
                name=name, defaults={"country": country, "founded_year": founded}
            )
            created += was_created
        self.stdout.write(self.style.SUCCESS(f"Seed complete: {created} new manufacturers."))
