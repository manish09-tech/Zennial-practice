import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import requests
import json
import uuid
from config.settings import (
    Base_url,
    NEWS_API_KEY,
    DEFAULT_QUERY,
    QUEUE_DIR,
    LOG_DIR,
    PAGE_SIZE,
    MAX_PAGES
)
from utiles.image_handler import handle_article_image
from utiles.logger import get_logger
from datetime import datetime, timezone
from tqdm import tqdm
from pymongo import MongoClient



logger = get_logger(__name__)

# MongoDB setup
Mongo_Url = "mongodb+srv://manishsaijakkula:Manishj09@news-article.jjyhq8r.mongodb.net/"
DATABASE_NAME = "news_database"
COLLECTION_NAME = "news_articles"

client = MongoClient(Mongo_Url)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def ensure_directores():
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(QUEUE_DIR, exist_ok=True)


def fetch_articles(query):
    all_articles = []

    for page in range(1, MAX_PAGES + 1):
        params = {
            "q": query,
            "pageSize": PAGE_SIZE,
            "page": page,
            "apikey": NEWS_API_KEY
        }

        response = requests.get(Base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if "articles" in data:
            all_articles.extend(data["articles"])
            logger.info(f"Fetching the page : {page} -> {response.status_code} -> {response.url}")
        else:
            logger.info(f"Page {page} : Does not have articles ")

    return all_articles 


def save_articles(article):
    article_id = str(uuid.uuid4())
    article["fetched_at"] = datetime.now(timezone.utc).isoformat()

    folder_path = os.path.join(QUEUE_DIR, article_id)
    os.makedirs(folder_path, exist_ok=True)

    image_path = handle_article_image(article.get('urlToImage'), folder_path, article_id)
    article["article_image_original"] = image_path.replace("\\", "/")

    json_path = os.path.join(folder_path, f"{article_id}.json")

    try:  
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(article, f, indent=4)
        logger.info(f"Saved article to {json_path}")
    except Exception as e:
        logger.error(f"Error saving article {article_id}: {e}")

    # Insert article into MongoDB
    try:
        article["_id"] = article_id  
        collection.insert_one(article)
        logger.info(f"Inserted article {article_id} into MongoDB")
    except Exception as e:
        logger.error(f"Error inserting article {article_id} into MongoDB: {e}")


def main():
    ensure_directores()
    logger.info("Starting fetch for api....")

    # Fetch Articles
    articles = fetch_articles(query=DEFAULT_QUERY)
    logger.info(f"Total Fetched Articles are {len(articles)}")

    # Save Articles in Folder and MongoDB
    for article in enumerate(tqdm(articles, desc="Saving Articles")):
        if article.get("title") and article.get("url"):
            save_articles(article)


if __name__ == "__main__":
    main()
