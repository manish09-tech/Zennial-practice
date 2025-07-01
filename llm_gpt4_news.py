import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurations
NEWS_URL = ""
OUTPUT = "news_articles.json"

def download_news_article(search_text, page_size=10):

    parameters = {
        "query": search_text,
        "pageSize": page_size,
        "language": "en"
    }

    response = requests.get(NEWS_URL, parameters=parameters)
    articles = response.json()["articles"]
    return articles

def save_news_article(articles, output_file=OUTPUT):
   
    output = {
        "status": "ok",
        "total_articles": len(articles),
        "articles": []
    }

    for article in articles:
        output["articles"].append({
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "content": article.get("content", "")
        })

    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Articles saved to {output_file}")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    articles = download_news_article(search_text="Trump India-US trade deal", page_size=10)
    save_news_article(articles)