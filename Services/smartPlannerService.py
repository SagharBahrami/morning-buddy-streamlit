import os
from dotenv import load_dotenv
import requests
from datetime import datetime, date
from pprint import pprint
load_dotenv()


class SmartPlanner():
    
    def __init__(self):
        
        self.api_key=os.getenv("SerpApi_API_KEY")
        
        if not self.api_key:
            
            raise ValueError("SerpApi API Key is required")
        self.base_url="https://serpapi.com/search?engine=google"
        
    def smart_planner(self, city: str, selected_date: date, limit: int=5):
        
        params={
            "q": f"events in {city} on {selected_date}", 
            "location": city,
            "api_key": self.api_key
        }
        
        response=requests.get(self.base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        events = data.get("events_results", [])

        cleaned_events = []
        
        for event in events[:limit]:
            event_date = event.get("date")

            if isinstance(event_date, dict):
                event_date = event_date.get("when")

            address = event.get("address", [])

            cleaned_events.append({
                "title": event.get("title"),
                "date": event_date,
                "venue_name": address[0] if isinstance(address, list) and len(address) > 0 else None,
                "street_address": address[1] if isinstance(address, list) and len(address) > 1 else None,
                "link": event.get("link"),
                "ticket_info": event.get("ticket_info"),
            })
            return cleaned_events