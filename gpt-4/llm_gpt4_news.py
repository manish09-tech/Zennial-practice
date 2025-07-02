import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurations
NEWS_URL = "https://newsapi.org/v2/everything"
API_KEY = "f639346990a34776916673d5e3548c28"

def download_news_article(search_text, page_size=10):
    params = {
        "q": search_text,
        "pageSize": page_size,
        "apiKey": API_KEY
    }

    response = requests.get(NEWS_URL, params=params)
    response.raise_for_status()  
    articles = response.json().get("articles", [])
    return articles

def save_articles(articles, base_filename="news_article"):
    for idx, article in enumerate(articles, start=1):
        output = {
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "content": article.get("content", "")
        }
        filename = f"{base_filename}_{idx}.json"
        with open(filename, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Saved {filename}")

if __name__ == "__main__":
    articles = download_news_article(search_text="Trump India-US trade deal", page_size=10)
    save_articles(articles)
