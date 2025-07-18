
# GPT-2 / GPT-4 Masterclass  
**Tokens · Embeddings · Vector Search · FAISS · MongoDB · FastAPI**

---

## Overview

GPT (Generative Pretrained Transformer) is a language model trained to generate human-like text.  
It's called “generative” because it can create text, code, summaries, and more from input prompts.  
Being “pretrained,” it learns from vast text datasets before fine-tuning or usage in real apps.  
This guide explains how GPT uses tokens and embeddings to understand and process language.  
You’ll use FAISS to store and search embeddings, and MongoDB to manage related text data.  
FastAPI wraps everything into a working AI application ready for deployment or experimentation.

---

## Table of Contents

1. [Tokens in GPT](#1-tokens-in-gpt)  
2. [Embeddings with GPT](#2-embeddings-with-gpt)  
3. [Vector-Based Search](#3-vector-based-search)  
4. [FAISS for Similarity](#4-faiss-for-similarity)  
5. [MongoDB for Storage](#5-mongodb-for-storage)  
6. [FastAPI for Serving](#6-fastapi-for-serving)

---

## 1. Tokens in GPT

### 🔍 What is GPT?

- **Generative**: Creates human-like responses.
- **Pretrained**: Trained on large datasets.
- **Transformer**: Uses attention to understand context.

---

### 🧠 What is a Model? (LLM)

A **model** is a trained function that maps inputs to outputs.  
An **LLM (Large Language Model)** is a model trained on billions of text tokens.

- Understands complex language tasks.
- Can generate summaries, answers, code, and more.

### 🧪 Code: Query GPT-4 (LLM)

```python
import openai
openai.api_key = "API_KEY"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is a Large Language Model?"}]
)
print(response['choices'][0]['message']['content'])
```

---

### 🧩 What are Tokens?

GPT models break text into tokens (words, subwords, or characters).

> `"Hello GPT World!"` → tokens → token IDs

### 🧪 Code: Tokenize Text

```python
from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
text = "Hello GPT World!"
tokens = tokenizer.tokenize(text)
ids = tokenizer.encode(text)

print("Tokens:", tokens)
print("Token IDs:", ids)
```

---

## 2. Embeddings with GPT

Embeddings are high-dimensional vectors that represent text meaning numerically.

> Used for semantic search, recommendation, clustering.

### 🧪 Code: Generate Embedding

```python
import openai
openai.api_key = "API_KEY"

res = openai.Embedding.create(
    input="What is AI?",
    model="text-embedding-ada-002"
)
embedding = res["data"][0]["embedding"]
print(embedding[:10])
```

---

## 3. Vector-Based Search

Instead of keywords, use **semantic similarity** to compare vectors.

> "Cute cats" ~ "Lovely kittens" (even without shared words)

### 🔢 Cosine Similarity Formula

```python
def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = sum(a**2 for a in vec1)**0.5
    mag2 = sum(b**2 for b in vec2)**0.5
    return dot / (mag1 * mag2)

vec1 = [2, 0, 1]
vec2 = [1, 1, 1]
print(f"Similarity: {cosine_similarity(vec1, vec2):.4f}")
```

**Output:**
```
Similarity: 0.7746
```

---

## 4. FAISS for Similarity

**FAISS** is used to store and search millions of embeddings efficiently using L2 or cosine metrics.

### 📦 Workflow

1. Convert text → embeddings  
2. Store in FAISS index  
3. Query embedding → search top K

### 🧪 Code: Build FAISS Search

```python
import openai, faiss, numpy as np
openai.api_key = "API_KEY"

texts = [
    "What is AI?",
    "Machine learning basics",
    "Future of tech in education",
    "Best places to visit in Europe"
]

def get_embedding(text):
    res = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return np.array(res["data"][0]["embedding"], dtype="float32")

embeddings = np.array([get_embedding(t) for t in texts])
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

query = "Travel destinations in Europe"
query_vec = get_embedding(query).reshape(1, -1)
distances, indices = index.search(query_vec, k=2)

print("Query:", query)
for i, idx in enumerate(indices[0]):
    print(f"{i+1}: {texts[idx]} (Distance: {distances[0][i]:.4f})")
```

---

### Sample Output (JSON-style)

```json
{
  "query": "Travel destinations in Europe",
  "results": [
    {
      "match_rank": 1,
      "text": "Best places to visit in Europe",
      "distance": 0.0000
    },
    {
      "match_rank": 2,
      "text": "Future of tech in education",
      "distance": 0.6724
    }
  ]
}
```

---

## 5. MongoDB for Storage

You can store text, metadata, and vectors in MongoDB for filtering and fast lookup.

### 🧪 Code: Insert Documents

```python
from pymongo import MongoClient

client = MongoClient("mongodb+srv://<username>:<password>@cluster.mongodb.net/")
db = client["practise_db"]
collection = db["employees"]

collection.insert_many([
    {"name": "Rahul", "city": "HYD", "salary": 25000, "address": {"street": "filmnagar", "pin_code": 500039}},
    {"name": "Umesh", "city": "HYD", "salary": 30000, "address": {"street": "bandra", "pin_code": 500045}},
    {"name": "Roopesh", "city": "HYD", "salary": 55000, "address": {"street": "filmnagar", "pin_code": 500039}}
])

print("Done!")
```

---

## 6. FastAPI for Serving

Use FastAPI to expose your GPT-based system via HTTP endpoints.

### 🧪 Code: GPT Chat Endpoint

```python
from fastapi import FastAPI, Request
import openai

openai.api_key = "API_KEY"
app = FastAPI()

@app.post("/chat/")
async def chat(req: Request):
    data = await req.json()
    prompt = data.get("text")

    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"response": res["choices"][0]["message"]["content"]}
```

---

## ✅ Summary

| Tool       | Purpose                            |
|------------|------------------------------------|
| **GPT-4**  | Language generation & understanding |
| **Tokens** | Smallest units GPT processes        |
| **Embeddings** | Vectors capturing text meaning |
| **FAISS**  | Fast vector similarity search       |
| **MongoDB**| Stores text + metadata + vectors    |
| **FastAPI**| Wraps everything in a deployable API|

---


## 💬 Questions

1. How do transformer models use self-attention for context understanding?
2. What are subword tokens, and why are they useful in GPT models?
3. How does GPT-4 differ in architecture from GPT-2?
4. What are the benefits of using FAISS over brute-force search?
5. How can you store and retrieve documents based on embedding similarity?
6. What is the role of `IndexFlatL2` in FAISS?
7. How would you use vector indexes for question answering?
8. How do embeddings improve search quality over keyword-based methods?
9. What are common methods to reduce vector dimensionality?
10. How can you cluster similar text documents using embeddings?
11. What are best practices for storing metadata with vectors in MongoDB?
12. How do you deploy a FastAPI app with GPU support?
13. How can FastAPI be used to expose multiple AI models?
14. What is the tradeoff between cosine and Euclidean distance in vector search?
15. How can you implement hybrid search (text + vector) in MongoDB?
16. How do you handle large-scale embedding storage and retrieval efficiently?
17. What are common issues when using FAISS with dynamic data?
18. How can you stream responses from GPT using FastAPI?
19. What are the rate limits and best practices for the OpenAI API?
20. How do you test the semantic similarity between user queries and stored documents?
"""
