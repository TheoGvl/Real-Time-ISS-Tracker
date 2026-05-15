# Real-Time ISS Tracker

An advanced, live-tracking application built with Python and Flet (v0.80+). This tool provides the exact real-time coordinates of the International Space Station (ISS) by polling the Open Notify API.

## Features

* **Live Updates:** Automatically fetches new coordinates every 3 seconds without requiring user interaction.
* **Multithreaded Architecture:** Uses Python's `threading` library to handle API requests in the background, ensuring the UI remains smooth and responsive.
* **Radar "Ping" Animation:** Features a visual feedback loop where the satellite icon flashes green upon every successful data sync.
* **Sub-Satellite Point Mapping:** Includes a direct link to Google Maps to visualize exactly what is on the Earth's surface directly beneath the station.
* **Modern Space UI:** A dark-themed, glassmorphism-inspired interface with high-contrast data cards and material icons.

## Tech Stack

* **Language:** Python 3.x
* **UI Framework:** Flet Utilizing modern `ft.Icons`, `ft.Colors`, and `ft.BoxFit` syntax.
* **Concurrency:** `threading` for background tasks.
* **Networking:** `requests` library.
* **External API:** [Open Notify ISS API](http://open-notify.org/Open-Notify-API/ISS-Location-Now/).

## How to Run Locally

  **Download the Project:**
    Save the `iss_track.py` file to your computer.

  **Install Dependencies:**
    Make sure you have Python and the required libraries:
    ```bash
    pip install flet requests
    ```

  **Run the Application:**
    Execute the script from your terminal:
    ```bash
    python iss_track.py
    ```

## Project Structure
* `iss_track.py`: Contains the main application logic, the background threading loop, and the reactive UI components.

## Potential Enhancements coming soon
* **Reverse Geocoding:** Integrate an API to display the name of the country or ocean the ISS is currently flying over.
* **Crew Information:** Add a section to show how many people are currently on board the ISS.
* **Overhead Alerts:** Use the user's location to notify them when the ISS is about to pass over their city.
