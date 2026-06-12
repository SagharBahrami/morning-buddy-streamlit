import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class WeatherService:
    
    def __init__(self):
        
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            
            raise ValueError("OPENWEATHER_API_KEY is required to initialize WeatherService")
        
        self.base_url="https://api.openweathermap.org/data/2.5/weather"
        
        
    def get_current_weather(self, city: str):
        params={
            "q": city,
            "appid": self.api_key,
            "units": "imperial"}
        
        response=requests.get(self.base_url, params=params)
        response.raise_for_status()
        
        data=response.json()
            
        cleaned_data={
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p"),
        "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")
        }
        return cleaned_data
