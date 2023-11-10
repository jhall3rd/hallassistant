import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Get the API key from https://openweathermap.org/api
API_KEY = os.environ.get("WEATHER_API_KEY")

# Get the weather forecast for London
url = "https://api.openweathermap.org/data/2.5/weather?q=London&appid=" + API_KEY
response = requests.get(url)

# Parse the JSON response
weather_data = response.json()



# Print the weather forecast
print("The weather forecast for London is:")
print("Temperature:", weather_data["main"]["temp"])
print("Humidity:", weather_data["main"]["humidity"])
print("Wind speed:", weather_data["wind"]["speed"])
