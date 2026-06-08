import os
from dotenv import load_dotenv
import requests
load_dotenv()


class NewsService():
    
    def __init__(self):
        
        self.api_key=os.getenv("NEWS_API_KEY")
        
        if not self.api_key:
            
            raise ValueError("News API Key is required to initialize NewsService")
        
        self.base_url = "https://newsapi.org/v2/everything"
        
    def get_news_by_topic(self, topic: str, language: str='en', page_size: int=5):
        
        params={
            "q":topic,
            "language": language,
            "pageSize": page_size,
            "apiKey": self.api_key
            
        }
        
        response=requests.get(self.base_url, params=params)
        response.raise_for_status()
        
        data=response.json()
        articles=data.get("articles", [])
        
        cleaned_articles=[]
        for article in articles:
            cleaned_articles.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "source": article.get("source", {}).get("name"),
                "url": article.get("url")
                
            })           
            
        return cleaned_articles