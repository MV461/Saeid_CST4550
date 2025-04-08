# wifispots.py
# app/management/commands/wifispots.py
import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from war_drive_app.models import WiFi  # Adjust if your app name is different
from datetime import datetime




class Command(BaseCommand):
    help = 'Load data from WiFi Spots CSV file (only records with Type WIFI)'

    def handle(self, *args, **kwargs):
        # Build full path to the CSV file
        data_file = os.path.join(settings.BASE_DIR, 'data', 'WigleWifi_20250327014237.csv')
        records = []

        try:
            # Use utf-8-sig encoding to handle any Byte-Order Mark (BOM)
            with open(data_file, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Filter: only keep records where the Type column equals 'WIFI'
                    if row['Type'].strip().upper() == 'WIFI':
                        records.append(row)
        except Exception as e:
            self.stderr.write(f"Error reading CSV file: {e}")
            return


        for row in records:
            # Process only those records where SSID is available.
            ssid_value = row['SSID'].strip()
            if ssid_value == '':
                # Skip records that don't have an SSID
                continue

            SSID = ssid_value  # Use SSID as is; do not fall back to MAC
            
            try:
                # Parse latitude and longitude from the CSV fields (they are provided as separate columns)
                latitude = float(row['CurrentLatitude'])
                longitude = float(row['CurrentLongitude'])
            except Exception as e:
                self.stderr.write(f"Error parsing coordinates for {SSID}: {e}")
                continue

            # Parse extra fields:
            try:
                # Convert the FirstSeen field (format: "2025-03-26 06:25:08") to a datetime
                first_seen_str = row['FirstSeen'].strip()
                first_seen = datetime.strptime(first_seen_str, '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                self.stderr.write(f"Error parsing FirstSeen for {SSID}: {e}")
                first_seen = None

            auth_mode = row['AuthMode'].strip()

            # Create or update the record based on the SSID.
            obj, created = WiFi.objects.get_or_create(
                SSID=SSID,
                defaults={
                    'latitude': latitude,
                    'longitude': longitude,
                    'firstSeen': first_seen,
                    'authMode': auth_mode,
                }
            )
            if not created:
                # Optionally update the record if it already exists.
                obj.latitude = latitude
                obj.longitude = longitude
                obj.firstSeen = first_seen
                obj.authMode = auth_mode
                obj.save()

        self.stdout.write("CSV data imported successfully (only WIFI records).")


