from django.core.management.base import BaseCommand
from war_drive_app.models import WiFi  # Adjust if needed

class Command(BaseCommand):
    help = 'Delete all WiFi records from the database.'

    def handle(self, *args, **kwargs):
        count, _ = WiFi.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} WiFi records from the database."))