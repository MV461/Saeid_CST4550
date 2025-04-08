from django.shortcuts import render
import folium 
# from folium.plugins import FastMarkerCluster
from folium.plugins import MarkerCluster
from war_drive_app.models import  WiFi

# Create your views here.

def index(request):
    WiFiSpots = WiFi.objects.all()

    # Create a Folium map centered at a default location
    # For example, using coordinates from your sample (adjust as necessary)
    m = folium.Map(location=[25.2048, 55.2708], zoom_start=12)

        # Create a MarkerCluster layer and add it to the map.
    marker_cluster = MarkerCluster().add_to(m)
    
    # Loop through each WiFi spot and add a marker with a custom popup.
    for WiFiSpot in WiFiSpots:
        coordinates = (WiFiSpot.latitude, WiFiSpot.longitude)
        popup_html = (
            f"<b>SSID:</b> {WiFiSpot.SSID}<br>"
            f"<b>First Seen:</b> {WiFiSpot.firstSeen}<br>"
            f"<b>Encryption:</b> {WiFiSpot.authMode}<br>"
        )
        folium.Marker(
            location=coordinates,
            popup=popup_html,
            icon=folium.Icon(color='blue')
        ).add_to(marker_cluster)
    
    
    # latitudes = [WiFiSpot.latitude for WiFiSpot in WiFiSpots]
    # longitudes = [WiFiSpot.longitude for WiFiSpot in WiFiSpots]
    
    
    # for WiFiSpot in WiFiSpots:
    #     coordinates = (WiFiSpot.latitude, WiFiSpot.longitude)
        
    #     # Build an HTML string for the popup
    #     popup_html = (
    #         f"<b>SSID:</b> {WiFiSpot.SSID}<br>"
    #         f"<b>FirstSeen:</b> {WiFiSpot.firstSeen}<br>"
    #         f"<b>AuthMode:</b> {WiFiSpot.authMode}"
    #     )
        
    #     # Add the marker with the custom popup to the map.
    #     folium.Marker(
    #         location=coordinates,
    #         popup=popup_html,
    #         icon=folium.Icon(color='blue')
    #     ).add_to(m)

   

    # FastMarkerCluster(data=list(zip( latitudes, longitudes))).add_to(m)

    # Pass the generated HTML representation of the map to the template.
    context = {'map': m._repr_html_()}
    return render(request, 'index.html', context)
