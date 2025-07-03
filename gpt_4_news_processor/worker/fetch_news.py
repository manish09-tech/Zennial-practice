import os
import requests
import json
import uuid

from utils.logger import get_logger
from config.settings import BASE_URL, NEWS_API_KEY, DEFAULT_KEY,MAX_PAGES,QUEUE_DIR,LOD_DIR,PAGE_SIZE

logger = get_logger("fetch_news")

def fetch_articles(query):
    
    params = {
        "q" : query,
        "page_size" : PAGE_SIZE,
        "page": 1,
        "apikey": NEWS_API_KEY
    }

def main():
    logger.info("starting fetch for api")

    # fetch articles
    articles = fetch_articles(query = DEFAULT_KEY)
    logger.info(f"total articles are {len(articles)}")

# save article
def save_article(articles):


if __name__ == "__main":
    main()
