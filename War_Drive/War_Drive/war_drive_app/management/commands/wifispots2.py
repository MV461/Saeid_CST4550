import os
import pandas as pd
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone
from war_drive_app.models import WiFi
from datetime import datetime

class Command(BaseCommand):
    help = 'Bulk import clean WiFi data using pandas'

    def handle(self, *args, **kwargs):
        call_command('cleardb')
        data_file = os.path.join(settings.BASE_DIR, 'data', 'combinedWiFi.csv')
        try:
            df = pd.read_csv(data_file, header=[0])
        except Exception as e:
            self.stderr.write(f"Error reading CSV: {e}")
            return

        wifi_objects = []

        for _, row in df.iterrows():
            try:
                wifi = WiFi(
                    SSID=row['SSID'],
                    latitude=float(row['CurrentLatitude']),
                    longitude=float(row['CurrentLongitude']),
                    firstSeen=timezone.make_aware(datetime.strptime(row['FirstSeen'], '%Y-%m-%d %H:%M:%S')),
                    authMode=row['AuthMode']
                )
                wifi_objects.append(wifi)
            except Exception as e:
                self.stderr.write(f"Skipping row due to error: {e}")

        # Perform bulk create
        WiFi.objects.bulk_create(wifi_objects)

        self.stdout.write(self.style.SUCCESS(f"Successfully bulk imported {len(wifi_objects)} WiFi records."))
