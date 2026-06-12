
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from datetime import datetime, date


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
                
       
        
        prompt = f"""
        Create a friendly weather summary using this information:

        City: {weather_data["city"]}
        Country: {weather_data["country"]}
        Temperature: {weather_data["temperature"]}
        Condition: {weather_data["condition"]}
        Humidity: {weather_data["humidity"]}
        Wind speed: {weather_data["wind_speed"]}
        Sunrise: {weather_data["sunrise"]}
        Sunset: {weather_data["sunset"]}
        Requirements:
        - Start with this title format: Weather Info: Here's your weather update for {weather_info["city"]}, {weather_info["country"]}!
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
    
    def create_smart_plan(self, event_data: dict, weather_data: dict, selected_date: date):
        
        
        title=f"✨ Your Personalized Day Plan for {weather_data['city']}({selected_date})"
        
        
        prompt = f"""
        You are a smart daily planner. Create a one-day plan for the user based on the current weather.

        Weather information:
        City: {weather_data['city']}
        Country: {weather_data['country']}
        Temperature: {weather_data['temperature']}
        Condition: {weather_data['condition']}
        Humidity: {weather_data['humidity']}
        Wind speed: {weather_data['wind_speed']}
        Sunrise: {weather_data['sunrise']}
        Sunset: {weather_data['sunset']}
        
        Event information:
        
        {event_data}
        

        Format the response in Markdown.

        Requirements:
        - Use this exact title: # {title}
        - Create exactly 4 sections including appropriate emoji with following headers:
        ### Morning Plan (9:00 AM - 12:00 PM)
        ### Lunch Plan (12:00 PM - 1:30 PM)
        ### Afternoon Plan (1:30 PM - 5:30 PM)
        ### Evening Plan (5:30 PM - 9:00 PM)
        
        - find the best events in {event_data} for {selected_date}
        - Suggest tourist attractions or activity types that fit the weather
        - Suggest whether lunch/dinner should be indoor or outdoor based on the weather
        - Suggest traditional or international food options
        - For events, concerts, or ticketed activities, do not invent links but search for any event or show and provide real link to get the ticket
        - Keep the plan practical, friendly, and easy to read
        - End with ✅ following with one short sentence about the day plan and wish them a nice and fun day
        """
            
        response=self.client.models.generate_content(
            model=self.text_model,
            contents=prompt,
            
        )
        return response.text.strip()
    