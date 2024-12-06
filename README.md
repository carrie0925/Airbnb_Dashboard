# Airbnb Dashboard

This project provides an interactive dashboard for Airbnb data analysis in New York City. The dashboard includes visualizations for crime rates, pricing trends, room types, and potential tourist revenue in different boroughs of NYC.

<div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
  <img src="image/airbnb_logo.png" alt="Airbnb Logo" width="150">
  <img src="image/Flag_of_New_York_City.png" alt="NYC Flag" width="150">
</div>

---

## Features

- 🗺️ Interactive Map: Visualizes borough-level data.
- 📊 Bar and Line Charts: Displays average prices and property counts.
- 🏙️ Crime Rate Comparisons: Highlights differences across boroughs.
- 🏡 Room Type Insights: Analyzes room types and pricing trends.

---

## Requirements

Before starting, ensure you have the following installed:

- **Python 3.8 or later**
- **SQLite** (if modifying the database)
- **Web Browser** (Chrome recommended)

---

## Installation

### Remember to install git first before below steps

### 1. Clone the Repository

git clone https://github.com/carrie0925/Airbnb_Dashboard.git
cd Airbnb_Dashboard

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Set Up Environment Variables

DOTENV_PATH=<path to your .env file>  
DB_PATH=<path to your .database file>  
IMAGE_PATH=<path to your .image files>  
LOGO_PATH=<path to your logo .image file>  
NYC_PATH=<path to your NYC .image file>
BOROUGH_IMAGES_PATH=<path to your BOROUGH_IMAGES .image file>

-For example:  
DB_PATH=C:/Users/YourUsername/Airbnb_Dashboard/data_final.db  
IMAGE_PATH=C:/Users/YourUsername/Airbnb_Dashboard/image/map_final.jpg

## Running the Application

### 1.Open dashboard

python app.py

### 2.Access the Dashboard

-http://127.0.0.1:8050/

### Seperate chart

-python fig_crime.py
-python fig_price.py
-python fig_room.py
-python fig_tourist.py

---

## Usage

- Explore the interactive map to view data at the borough level.
