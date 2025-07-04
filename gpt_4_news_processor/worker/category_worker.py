import os
import sys
import json
from tqdm import tqdm
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Setup Directories
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
QUEUE_DIR = os.path.join(BASE_DIR, "queue")
ARTICLE_STORE_BASE = os.path.join(BASE_DIR, "article_store")

INPROGRESS_DIR = os.path.join(ARTICLE_STORE_BASE, "inprogress")
COMPLETED_DIR = os.path.join(ARTICLE_STORE_BASE, "completed")
FAILED_DIR = os.path.join(ARTICLE_STORE_BASE, "failed")

for directory in [QUEUE_DIR, INPROGRESS_DIR, COMPLETED_DIR, FAILED_DIR]:
    os.makedirs(directory, exist_ok=True)

#  Load GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Categories
CATEGORIES = [
    "Politics", "Finance", "Health", "Science",
    "Technology", "Sports", "Crypto Currency",
    "Other", "Entertainment"
]

# Prompts
CATEGORY_PROMPT = (
    "Given the title, description, content of a news article, identify the most suitable category from the list: "
    f"{', '.join(CATEGORIES)}. If none matches then return 'Other'.\n\n"
    "Title: {title}\nDescription: {description}\nContent: {content}\nCategory:"
)

RAW_CATEGORY_PROMPT = (
    "Given the title, description, and content of a news article, suggest a synthetic category name "
    "that best describes its subject. E.g. 'Crypto', 'Climate News'.\n\n"
    "Title: {title}\nDescription: {description}\nContent: {content}\nSuggested Category:"
)

def get_category_from_gpt2(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(
        inputs,
        max_length=inputs.shape[1] + 20,
        num_return_sequences=1,
        do_sample=True,
        top_p=0.9,
        top_k=50
    )

    result = tokenizer.decode(output[0], skip_special_tokens=True)

    result_lines = result.split("Category:") if "Category:" in result else result.split("Suggested Category:")

    if len(result_lines) > 1:
        return result_lines[1].strip().split("\n")[0]
    else:
        return result.strip()

def process_articles(article_id):
    folder_path = os.path.join(QUEUE_DIR, article_id)
    article_json_file = os.path.join(folder_path, f"{article_id}.json")

    if not os.path.exists(article_json_file):
        print(f"[SKIP] {article_json_file} does not exist.")
        return
    
    with open(article_json_file, "r", encoding="utf-8") as f:
        try:
            article_json = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to parse JSON for article {article_id}: {e}")
            return

    title = article_json.get("title", "")
    description = article_json.get("description", "")
    content = article_json.get("content", "")

    category_prompt = CATEGORY_PROMPT.format(title=title, description=description, content=content)
    raw_category_prompt = RAW_CATEGORY_PROMPT.format(title=title, description=description, content=content)

    recommended_category = get_category_from_gpt2(category_prompt)
    gpt4_suggestion_category = get_category_from_gpt2(raw_category_prompt)

    article_json['recommended_category'] = recommended_category
    article_json['gpt4_suggestion_category'] = gpt4_suggestion_category

    completed_folder = os.path.join(COMPLETED_DIR, article_id)
    os.makedirs(completed_folder, exist_ok=True)
    completed_json_file = os.path.join(completed_folder, f"{article_id}.json")

    with open(completed_json_file, "w", encoding="utf-8") as f:
        json.dump(article_json, f, indent=2)

    print(f"[DONE] Processed article {article_id}")

def generate_sample_articles():
    print("[INFO] Generating sample test articles...")
    for i in range(1, 16):
        article_id = f"news_article_{i}"
        folder = os.path.join(QUEUE_DIR, article_id)
        os.makedirs(folder, exist_ok=True)
        article_data = {
            "title": f"Breaking News {i}",
            "description": f"This is a short description of the news article {i}.",
            "content": f"Full content of article {i}. This article discusses topics relevant to test category classification."
        }
        with open(os.path.join(folder, f"{article_id}.json"), "w", encoding="utf-8") as f:
            json.dump(article_data, f, indent=2)

def main():
    article_folders = [
        name for name in os.listdir(QUEUE_DIR)
        if os.path.isdir(os.path.join(QUEUE_DIR, name))
    ]

    if not article_folders:
        generate_sample_articles()
        article_folders = [
            name for name in os.listdir(QUEUE_DIR)
            if os.path.isdir(os.path.join(QUEUE_DIR, name))
        ]

    print(f"[INFO] {len(article_folders)} articles available to process.")

    for article_id in tqdm(article_folders, desc="Categorizing articles"):
        process_articles(article_id)

if __name__ == "__main__":
    main()
