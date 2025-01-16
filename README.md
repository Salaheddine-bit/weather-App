# Weather Forecast Application

A weather forecast application built using Python and CustomTkinter. It allows users to fetch and visualize weather data such as temperature, humidity, and wind speed, along with a 7-day forecast. Users can also save and load weather data in JSON format.

---

## Features

- **Search Weather**: Enter a city name to fetch weather data using the Open-Meteo API.
- **Visualizations**:
  - Temperature trends.
  - Humidity trends.
  - Wind speed trends.
- **7-Day Forecast**:
  - Displays daily weather with icons, max/min temperature, and more.
- **Save/Load Data**:
  - Save weather data as JSON files.
  - Load previously saved JSON files to view data offline.

---

## Installation

### Requirements

- Python 3.8+
- Libraries:
  - `customtkinter`
  - `requests`
  - `pandas`
  - `matplotlib`
  - `Pillow`
---

## Usage

### Search Weather

1. Enter the city name in the input field.
2. Click **Rechercher** to fetch weather data.

### Visualize Data

- Use the buttons:
  - **Temp**: Visualize temperature trends.
  - **Humid**: Visualize humidity trends.
  - **vent**: Visualize wind speed trends.

### Save Data

- Click **Sauvegarder JSON** to save the current weather data as a JSON file in the `data` folder.

### Load Data

- Click **Charger JSON** to load a previously saved JSON file and display its data.

---

## Folder Structure

```
.
├── my projet.py             # Main application script
├── icon/              # Folder containing weather icons
├── data/              # Folder for saving JSON data

```

---

## Weather Icons

- The application uses weather icons stored in the `icon/` folder.
- Default icons will be displayed if a specific weather icon is unavailable.

---

## APIs Used

- **Open-Meteo API**:
  - Geocoding: Converts city names to coordinates.
  - Weather Data: Provides hourly and daily weather information.

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the application.

