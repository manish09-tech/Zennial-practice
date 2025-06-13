import requests
import logging
import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Model, GPT2Tokenizer

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = "f639346990a34776916673d5e3548c28"
HEADLINE_COUNT = 2
ARTICLE_COUNT = 4

logging.basicConfig(level=logging.INFO, format= "%(asctime)s - %(levelname)s - %(message)s")


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
embedding_model = GPT2Model.from_pretrained("gpt2")
head_model = GPT2LMHeadModel.from_pretrained("gpt2")

tokenizer.pad_token = tokenizer.eos_token
head_model.pad_token_id = head_model.config.eos_token_id

def get_mean_embedding(input_text):
    input_text_tokens = tokenizer(input_text, return_tensors="pt")
    with torch.no_grad():
        embeddings = embedding_model(**input_text_tokens)
    return embeddings.last_hidden_state.mean(dim=1)

def fetch_news_articles(api_key, count) -> list[dict]:
    logging.info ("Fetching new articles.. please wait" )
    news_api_response =requests.get(NEWS_API_URL, params = {
        "apikey" : api_key,
        "country" : "us",
        "pageSize" : count
    })

    news_api_response.raise_for_status()
    news_articles = news_api_response.json().get("articles", [])
    logging.info (f"Fetched {len(news_articles)} articles")
    return news_articles

if __name__ == "__main__":
    try:
        articles = fetch_news_articles(API_KEY, ARTICLE_COUNT)
        print (articles)
    except Exception as e:
        logging.info (str(e))