import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(city):
    request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&units=metric'

    weather_data = requests.get(request_url).json()

    return {
        "city": weather_data["name"],
        "temperature": weather_data["main"]["temp"],
        "feels like": weather_data["main"]["feels_like"],
        "description": weather_data["weather"][0]["description"],
    }

    