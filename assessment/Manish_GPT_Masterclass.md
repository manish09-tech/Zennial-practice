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
4. [faiss for Storing and Searching Text](#4-faiss-for-storing-and-searching-text)  
5. [Storing Vectors in MongoDB](#5-storing-vectors-in-mongodb)  
6. [FastAPI to Build AI Applications](#6-fastapi-to-build-ai-applications)

---

## 1. Tokens in GPT

### 🔍 What is GPT?

**GPT** stands for **Generative Pretrained Transformer**:

- **Generative**: It generates human-like text responses.
- **Pretrained**: Trained on massive datasets before use.
- **Transformer**: Uses self-attention to understand context in language.

---

### 🧠 What is a Model?

A **model** in machine learning is a mathematical function trained to recognize patterns and make predictions based on input data.

- In GPT's case, the model learns how words and sentences are formed.
- It maps **input tokens** (like words) to **output tokens** (like answers, code, or completions).
- Models have versions (like GPT-2, GPT-3.5, GPT-4), each trained with more data and better architecture.

> 💡 **Tip**: Larger models are more accurate but require more memory and processing power.

---

Before GPT can understand or generate anything, it first breaks the input into **tokens**, which are chunks of text (words, subwords, or characters).

**Example**: A sentence like `"Hello GPT World!"` is converted into token IDs before the model processes it.

> 💡 **Use Case**: Controlling token count is important for cost and performance when calling large models.

### 🧪 Code: Tokenizing Text

```python
from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
text = "Hello GPT World!"
tokens = tokenizer.tokenize(text)
ids = tokenizer.encode(text)

print("Tokens:", tokens)
print("Token IDs:", ids)
```

**Output:**
```
Tokens: ['Hello', 'ĠGP', 'T', 'ĠWorld', '!']
Token IDs: [15496, 50256, 22173, 0, 328]
```

---

## 2. Embeddings with GPT

Embeddings are numerical vectors that represent the meaning of text in a machine-understandable form.

**Example**: Google News and LinkedIn use embeddings to match articles or jobs with your interests — even when keywords differ.

> 💡 **Use Case**: Semantic search, chat memory, question answering, and recommendation systems.

### 🧪 Code: Generate Embeddings Using OpenAI API

```python
import openai

openai.api_key = "API_KEY"

response = openai.Embedding.create(
    input="What is AI?",
    model="text-embedding-ada-002"
)

embedding = response['data'][0]['embedding']
print("Vector:", embedding[:10])  # Show first 10 dimensions
```

**Output:**
```
Vector: [0.01827, -0.01295, 0.02183, -0.00715, 0.00675, -0.01925, 0.00435, -0.00098, 0.01234, -0.00519]
```

---

## 3. Vector-Based Search

Instead of using keywords, vector-based search matches items by **semantic meaning** using cosine similarity or distance metrics.

**Example**: "Laptop deals" could match documents like "Best Lenovo's under 50000 rupees" even if keywords differ.

> 💡 **Use Case**: Smart search bars, personalized product recommendations, document similarity engines.

### 🧪 Code: Cosine Similarity with NumPy

```python
sentence1 = "Cats are cute"
sentence2 = "Dogs are friendly"

embedding1 = [2, 0, 1]
embedding2 = [1, 1, 1]

def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = sum(a ** 2 for a in vec1) ** 0.5
    mag2 = sum(b ** 2 for b in vec2) ** 0.5
    return dot / (mag1 * mag2)

similarity = cosine_similarity(embedding1, embedding2)

print(f"Similarity: {similarity:.4f}")
```

**Output:**
```
Similarity: 0.7746
```

---

## 4. faiss for Storing and Searching Text

**FAISS** allows you to store millions of text embeddings and perform efficient similarity search.

Text is converted into embeddings using OpenAI or similar models, then stored in a FAISS index. Queries are embedded too, and matched against stored data.

**Example**: A query like `"Travel in Europe"` can return `"Best places to visit in Europe"` using semantic similarity.

> 💡 **Use Case**: AI search engines, content recommendations, chatbot memory.

### 🧪 Code: Store Text as Embeddings in FAISS

```python
import openai
import faiss
import numpy as np

openai.api_key = "API_KEY"

texts = [
    "What is AI?",
    "How does machine learning work?",
    "The future of technology in education",
    "Best places to visit in Europe"
]

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return np.array(response['data'][0]['embedding'], dtype='float32')

embeddings = np.array([get_embedding(t) for t in texts])
dimension = len(embeddings[0])

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

query = "Travel destinations in Europe"
query_embedding = get_embedding(query).reshape(1, -1)

distances, indices = index.search(query_embedding, k=2)

print("Query:", query)
for i, idx in enumerate(indices[0]):
    print(f"Match {i+1}: {texts[idx]} (Distance: {distances[0][i]:.4f})")
```

---

**🧾 Sample Output (JSON)**

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
      "text": "The future of technology in education",
      "distance": 0.6724
    }
  ]
}
```

---

## 5. Storing Vectors in MongoDB

After generating embeddings from text, you can store them in MongoDB along with metadata like category, tags, user ID, etc.

> 💡 **Use Case**: Search history, document labels, and filterable indexes in AI systems.

### 🧪 Code: Store and Filter Documents in MongoDB

```python
from pymongo import MongoClient

mongo_uri = "mongodb+srv://<username>:<password>@cluster.mongodb.net/"
client = MongoClient(mongo_uri)

db = client["practise_db"]
collection = db["employees"]

collection.insert_many([
    {"name": "Rahul", "city": "HYD", "salary": 25000, "address": {"street": "filmnagar", "pin_code": 500039}},
    {"name": "Umesh", "city": "HYD", "salary": 30000, "address": {"street": "bandra", "pin_code": 500045}},
    {"name": "Roopesh", "city": "HYD", "salary": 55000, "address": {"street": "filmnagar", "pin_code": 500039}},
])

print("Done!")
```

---
**Output:**
```
Done!

```

---

**MongoDB Document**
```json
[
  {
    "_id": ObjectId("..."),
    "name": "Rahul",
    "city": "HYD",
    "salary": 25000,
    "address": {
      "street": "filmnagar",
      "pin_code": 500039
    }
  },
  {
    "_id": ObjectId("..."),
    "name": "Umesh",
    "city": "HYD",
    "salary": 30000,
    "address": {
      "street": "bandra",
      "pin_code": 500045
    }
  },
  {
    "_id": ObjectId("..."),
    "name": "Roopesh",
    "city": "HYD",
    "salary": 55000,
    "address": {
      "street": "filmnagar",
      "pin_code": 500039
    }
  }
]

```

---


## 6. FastAPI to Build AI Applications

Use **FastAPI** to build backend endpoints that return GPT responses, embedding vectors, or search results.

**Example**: A POST endpoint that takes a question and returns a GPT-4 generated answer.

> 💡 **Use Case**: Deploy GPT into websites, dashboards, internal tools, or mobile apps.

### 🧪 Code: Chat Endpoint Using FastAPI

```python
from fastapi import FastAPI, Request
import openai

openai.api_key = "API_KEY"
app = FastAPI()

@app.post("/chat/")
async def chat(req: Request):
    data = await req.json()
    prompt = data.get("text")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response['choices'][0]['message']['content']
    return {"response": answer}
```

### 🛠 Run with:

```python
uvicorn app:app --reload
```

### 🔎 Sample Request:

```json
{
  "text": "What is AI?"
}
```

### ✅ Sample Response:

```json
{
  "response": "AI, or Artificial Intelligence, refers to the simulation of human intelligence in machines that are programmed to think and learn."
}
```