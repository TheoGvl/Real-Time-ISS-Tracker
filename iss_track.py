import flet as ft
import requests
import threading
import time
import webbrowser
from datetime import datetime

def main(page: ft.Page):
    # --- Window Configuration ---
    page.title = "Real-Time ISS Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 40
    page.window.width = 500
    page.window.height = 600
    page.bgcolor = "#0a0a1a" # Deep space background

    # --- UI Elements ---
    
    # 1. we create an Icon widget for the radar symbol. We use a satellite icon from Flet's built-in icons.
    radar_icon_img = ft.Icon(ft.Icons.SATELLITE_ALT, size=40, color=ft.Colors.BLUE_400)
    
    # 2. we wrap the radar icon in a Container to create a circular "radar blip" effect. We set the alignment to center the icon within the container, and we add a border that will animate when the ISS position updates.
    radar_icon = ft.Container(
        content=radar_icon_img,
        width=90, 
        height=90,
        alignment=ft.Alignment(0, 0),
        shape=ft.BoxShape.CIRCLE,
        border=ft.Border.all(2, ft.Colors.BLUE_900),
        animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT) # Smooth color transition
    )

    lat_text = ft.Text("Latitude: Loading...", size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)
    lon_text = ft.Text("Longitude: Loading...", size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)
    time_text = ft.Text("Last Update: --:--:--", size=14, color=ft.Colors.GREY_500)

    # Variables to hold the current coordinates for the map
    current_lat = ""
    current_lon = ""

    def open_map(e):
        if current_lat and current_lon:
            # Opens the default web browser to the exact coordinates on Google Maps
            url = f"https://www.google.com/maps/search/?api=1&query={current_lat},{current_lon}"
            webbrowser.open(url)

    map_btn = ft.ElevatedButton(
        "Open in Google Maps",
        icon=ft.Icons.MAP,
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        height=50,
        on_click=open_map,
        disabled=True # Disabled until we get our first valid coordinates
    )

    # The main stats card
    stats_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    radar_icon,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    lat_text,
                    lon_text,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    time_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=40,
            width=350,
            bgcolor="#15152a",
            border_radius=15,
            border=ft.Border.all(1, "#2a2a4a")
        ),
        elevation=10,
    )

    # --- Background Task (The "Real-Time" Loop) ---
    def fetch_iss_data():
        nonlocal current_lat, current_lon
        
        while True:
            try:
                # The Open Notify API for ISS Location
                response = requests.get("http://api.open-notify.org/iss-now.json", timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    current_lat = data["iss_position"]["latitude"]
                    current_lon = data["iss_position"]["longitude"]
                    
                    # Convert UNIX timestamp to readable local time
                    timestamp = data["timestamp"]
                    dt_object = datetime.fromtimestamp(timestamp)
                    
                    # Update UI texts
                    lat_text.value = f"Latitude: {current_lat}"
                    lon_text.value = f"Longitude: {current_lon}"
                    time_text.value = f"Last Update: {dt_object.strftime('%H:%M:%S')}"
                    
                    # Enable the map button since we have data
                    map_btn.disabled = False
                    
                    # Radar Flash Effect 
                    radar_icon.border = ft.Border.all(3, ft.Colors.GREEN_400)
                    radar_icon_img.color = ft.Colors.GREEN_400
                    page.update()
                    
                    # Wait 0.5 seconds, then return the radar to normal blue
                    time.sleep(0.5)
                    radar_icon.border = ft.Border.all(2, ft.Colors.BLUE_900)
                    radar_icon_img.color = ft.Colors.BLUE_400
                    page.update()

            except Exception as e:
                time_text.value = "Connection lost. Retrying..."
                page.update()

            # Wait 3 seconds before fetching the next position
            time.sleep(3)

    # Start the background loop in a separate thread so it doesn't freeze the Flet UI
    threading.Thread(target=fetch_iss_data, daemon=True).start()

    # --- Final Layout ---
    page.add(
        ft.Text(" ISS Tracker", size=35, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        ft.Text("Live position of the International Space Station", size=15, color=ft.Colors.GREY_400),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        
        stats_card,
        
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        map_btn
    )

# Run the app
ft.run(main) # type: ignore