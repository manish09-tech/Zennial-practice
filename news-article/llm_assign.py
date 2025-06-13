import requests 
import logging 
import torch
import torch.nn.functional as F
import json
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Model

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = "f639346990a34776916673d5e3548c28"
HEADLINE_COUNT = 5
ARTICLE_COUNT = 1

# Logging-config
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gen_model = GPT2LMHeadModel.from_pretrained("gpt2")
emb_model = GPT2Model.from_pretrained("gpt2")

tokenizer.pad_token = tokenizer.eos_token
gen_model.pad_token_id = gen_model.config.eos_token_id
emb_model.pad_token_id = emb_model.config.eos_token_id

def get_mean_embedding(input_text):
    input_tokens = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        output = emb_model(**input_tokens)
    return output.last_hidden_state.mean(dim=1)

def fetch_news_articles(api_key, count) -> list[dict]:
    logging.info("Fetching news articles...")
    response = requests.get(NEWS_API_URL, params={
        "apiKey": api_key,
        "country": "us",
        "pageSize": count
    })
    response.raise_for_status()
    articles = response.json().get("articles", [])
    logging.info(f"Fetched {len(articles)} articles")
    return articles


def generate_headlines(prompt):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = gen_model.generate(
        input_ids,
        do_sample=True,
        num_return_sequences=HEADLINE_COUNT,
        max_new_tokens=50,
        temperature=0.8,
        top_k=50,
        top_p=0.95
    )
    return [
        tokenizer.decode(output, skip_special_tokens=True).replace(prompt, "").strip() for output in outputs
    ]

def process_news_articles(news_articles):
    final_output = {
        "status": "ok",
        "news_articles": []
    }

    for news_article in news_articles:
        content = news_article.get("content", "")
        title = news_article.get("title", "")
        description = news_article.get("description", "")
        news_text = f"{title}. {description}. {content}".strip()

        if not news_text:
            continue

        prompt = f"Generate a headline for this news: {news_text} Headline:"
        generated_headlines = generate_headlines(prompt)
        news_text_embedding = get_mean_embedding(prompt)

        result = []
        for id, headline in enumerate(generated_headlines):
            headline_embedding = get_mean_embedding(headline)
            score = F.cosine_similarity(headline_embedding, news_text_embedding).item()
            result.append({
                "score": id + 1,  
                "text": headline
            })

        final_output["news_articles"].append({
            "title": title,
            "description": description,
            "content": content,
            "top 5 headlines": result
        })

    print(final_output)


if __name__ == "__main__":
    try:
        articles = fetch_news_articles(API_KEY, ARTICLE_COUNT)
        process_news_articles(articles)
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
