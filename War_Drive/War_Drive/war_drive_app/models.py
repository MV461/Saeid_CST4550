from django.db import models

# # Create your models here.
# class EVChargingLocation(models.Model):
#     station_name = models.CharField(max_length=250)
#     latitude = models.FloatField()
#     longitude = models.FloatField()

class WiFi(models.Model):
    SSID = models.CharField(max_length=100, blank=True)
    firstSeen = models.DateTimeField(blank=True, null=True)
    authMode = models.CharField(max_length=200, blank=True)
    
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.SSID