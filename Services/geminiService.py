
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
class GeminiService:
    
    def __init__(self):
        
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            
            raise ValueError("GOOGLE_API_KEY is required to initialize GeminiService")
        
        
        self.client = genai.Client(api_key=self.api_key)
        self.text_model = "gemini-3.1-pro-preview"
        self.image_model = "gemini-3.1-flash-image-preview"
    
    def get_thought_for_day(self):
        
        prompt = """
        Generate one short daily motivational thought for a productivity and smart planner app.

        Requirements:
        - Warm and encouraging tone
        - 1 sentence only
        - Maximum 25 words
        - No hashtags
        - No emojis
        - No quotation marks
        """
        response=self.client.models.generate_content(model=self.text_model,
                                                    contents=prompt,
                                                    config=types.GenerateContentConfig(
                                                        temperature=0.8
                                                    )
                                               )
        return response.text.strip()
    
    def get_image_for_thought(self, thought: str):
        
        prompt = f"""
        Generate a beautiful motivational nature image inspired by this sentence:

        {thought}

        Image requirements:
        - Realistic photography style, not illustration, not painting, not fantasy art
        - Natural lighting
        - Real-world scene
        - Calm and inspiring mood
        - Avoid overly magical or cartoon-like scenery
        - No text, no letters, no quotes, no watermark
        """
        response=self.client.models.generate_content(
            model=self.image_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"]
            )
        )
        
        for part in response.candidates[0].content.parts:
            
            if part.inline_data:
                return part.inline_data.data
            
        return None
    

    def get_weather_summary(self, weather_data: dict):
                
        city = weather_data["name"]
        country = weather_data["sys"]["country"]
        temperature = weather_data["main"]["temp"]
        condition = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        sunrise = datetime.fromtimestamp(weather_data["sys"]["sunrise"]).strftime("%I:%M %p")
        sunset = datetime.fromtimestamp(weather_data["sys"]["sunset"]).strftime("%I:%M %p")
        
        prompt = f"""
        Create a friendly weather summary using this information:

        City: {city}
        Country: {country}
        Temperature: {temperature}
        Condition: {condition}
        Humidity: {humidity}
        Wind speed: {wind_speed}
        Sunrise: {sunrise}
        Sunset: {sunset}

        Requirements:
        - Start with this title format: Weather Info: Here's your weather update for {city}, {country}!
        - Mention temperature, condition, humidity, and wind speed
        - Mention sunrise and sunset
        - Add one practical suggestion based on the weather
        - Keep it under 100 words
        """
        
        response=self.client.models.generate_content(
            model=self.text_model,
            contents=prompt,
            
        )
        return response.text.strip()
    
    def get_news_summary(self, news_data: dict):
        
        prompt = f"""
        Create a short, helpful summary from this news article information:

        Title: {news_data.get("title")}
        Source: {news_data.get("source")}
        Description: {news_data.get("description")}
        URL: {news_data.get("url")}

        Requirements:
        - At most 1 paragraph
        - Clear and beginner-friendly
        - Do not invent facts beyond the title and description
        - Mention that the user can open the link for the full article if needed
        """
        response=self.client.models.generate_content(
            model=self.text_model,
            contents=prompt
        )

        return response.text.strip()
    
    def create_smart_plan(self, city: str):
        return