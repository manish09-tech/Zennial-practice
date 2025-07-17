
# GPT Masterclass (GPT-2 / GPT-4)

## Overview

In this guide, I explore how GPT models work, including how they handle tokens and create embeddings. I also demonstrate how to use these embeddings for vector-based search using FAISS, store them in MongoDB, and build simple AI applications with FastAPI. The goal is to show how these tools can work together in real-world scenarios.


## Table of Contents

1. Tokens in GPT
2. Embeddings with GPT
3. Vector-Based Search
4. FAISS for Similarity Search
5. Storing Vectors in MongoDB
6. FastAPI to Build AI Applications


## 1. Tokens in GPT

Tokens are chunks of text (words, subwords, or characters) that GPT models process.

**Example**: When chatting with ChatGPT or a website bot, your message is split into tokens before the model understands it.

> **Use Case**: Token counting is critical for managing cost and performance in long chats or large document summaries.

### Example: Tokenizing Text

from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
text = "Hello GPT World!"
tokens = tokenizer.tokenize(text)
ids = tokenizer.encode(text)

print("Tokens:", tokens)
print("Token IDs:", ids)

# output: 
Tokens: ['Hello', 'ĠGP', 'T', 'ĠWorld', '!']
Token IDs: [15496, 50256, 22173, 0, 328]


## 2. Embeddings with GPT

Embeddings are numerical representations of text. GPT-4 uses these to understand relationships in text.

**Example**: LinkedIn and Google News recommend articles or jobs that are similar in meaning—not keywords—based on embeddings.

> **Use Case**: Matching queries with documents in semantic search systems.


### Example: Get Embeddings using OpenAI API

import openai

openai.api_key = "API_KEY"

response = openai.Embedding.create(
    input="What is AI?",
    model="text-embedding-ada-002"
)

embedding = response['data'][0]['embedding']
print("Vector:", embedding[:10])  # Print first 10 dims

# output: 
Vector: [0.01827407, -0.01295031, 0.02183194, -0.00715381, 0.00675101, -0.01925917, 0.00435264, -0.00098662, 0.01234759, -0.00519476]


## 3. Vector-Based Search

Search based on semantic similarity using cosine distance between embeddings.

**Example**: Amazon shows product suggestions like "Customers also viewed" based on vector similarity, not product names.

> **Use Case**: Product discovery, intelligent auto-complete, and document similarity engines.

### Example: Cosine Similarity with NumPy

# Step 1: Define two short vectors
sentence1 = "Cats are cute"
sentence2 = "Dogs are friendly"

embedding1 = [2, 0, 1]
embedding2 = [1, 1, 1]

# Step 2: Cosine similarity function
def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2)) #zip() is a built-in function that combines elements
    mag1 = sum(a ** 2 for a in vec1) ** 0.5
    mag2 = sum(b ** 2 for b in vec2) ** 0.5
    return dot / (mag1 * mag2)

# Step 3: Calculate and print similarity
similarity = cosine_similarity(embedding1, embedding2)

print(f"Sentence 1: {sentence1}")
print(f"Sentence 2: {sentence2}")
print(f"Cosine Similarity: {similarity:.4f} (1 = Very Similar, 0 = Different)")

# output: 
Sentence 1: Cats are cute  
Sentence 2: Dogs are friendly  
Cosine Similarity: 0.7746 (1 = Very Similar, 0 = Different)



## 4. FAISS for Similarity Search

FAISS helps you search through millions of embeddings efficiently.

**Example**: Spotify recommends songs by comparing vector embeddings of your listening history.

> **Use Case**: Personalized content feeds, document deduplication, fast nearest-neighbor search.

### Example: Basic FAISS Search

import faiss
import numpy as np

# Step 1: Dimension of vectors (2D)
d = 2

# Step 2: Create the index
index = faiss.IndexFlatL2(d)

# Step 3: Add some vectors to the index
data = np.array([[1, 1], [2, 2], [10, 10]]).astype('float32')
index.add(data)

# Step 4: Define a query vector
query = np.array([[1, 2]]).astype('float32')

# Step 5: Search for 2 nearest vectors
D, I = index.search(query, k=2)

print("Nearest indices:", I)
print("Distances:", D)

# output:
Nearest indices: [[1 0]]
Distances: [[1.0 1.0]]


## 5. Storing Vectors in MongoDB

Vectors can be stored with metadata for retrieval.

When we generate embeddings (vectors) from text using a model like GPT, we can store these vectors in a database — along with extra information, called metadata.

### Example: Store vectors in MongoDB

This metadata might include:

The original text, A category or label (e.g., "FAQ", "Product Description"), Tags (e.g., "AI", "support", "finance"), Date/time of creation, User ID, document ID, etc.

### Example: Store Embeddings in MongoDB


from pymongo import MongoClient

# MongoDB setup
mongo_cluster = "mongodb+srv://manishsaijakkula:********@news-article.jjyhq8r.mongodb.net/"

client = MongoClient(mongo_cluster)
database_name = "practise_db"
collection = "employees"

database = client[database_name]
employee_collection = database[collection]

 employee_collection.insert_many([
     {"name" : "Rahul", "city" : "HYD", "salary" : 25000, "address" : {"street": "filmnagar", "pin_code" : 500039}},
     {"name" : "Umesh", "city" : "HYD", "salary" : 30000, "address" : {"street": "bandra", "pin_code" : 500045}},
     {"name" : "Roopesh", "city" : "HYD", "salary" : 55000, "address" : {"street": "filmnagar", "pin_code" : 500039}}
 ])

employee_collection.delete_many({
    "address.pin_code" : {"$lt" : 500045}
})

print ("Done!!")

# output
id: 686cdf2952a66e40a884f961
name:"Rahul"
city:"HYD"
salary:25000
>address:Object
street:"filmnagar"
pin_code:500039

id: 686cdf2952a66e40a884f962
name:"Umesh"
city:"HYD"
salary:30000
>address:Object
street:"bandra"
pin_code:500045

id: 686cdf2952a66e40a884f963
name:"Umesh"
city:"HYD"
salary:55000
>address:Object
street:"filmnagar"
pin_code:500039


## 6. FastAPI to Build AI Applications

FastAPI makes it easy to build APIs for AI apps like chatbots, search, summarization, etc.

**Example**: Notion AI and Grammarly use FastAPI-like backends to process summarization, Q&A, or rephrasing tasks on the fly.

> **Use Case**: Deploying AI services as REST APIs for internal tools or web apps.

### Example: FastAPI Endpoint to Embed Text


from fastapi import FastAPI, Request
import openai

openai.api_key = "API_KEY"       # Replace this with your actual OpenAI key
app = FastAPI()                  # Create a FastAPI app

@app.post("/chat/")              # Define a POST endpoint at /chat/
async def chat(req: Request):    
    data = await req.json()      # Read the JSON data sent in the request
    prompt = data.get("text")    # Extract the "text" field from that data

    response = openai.ChatCompletion.create(     # Call OpenAI's chat API
        model="gpt-4",                  
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response['choices'][0]['message']['content']  # Extract the reply
    return {"response": answer}  # Return it as a JSON response


Run with:
## cmd
uvicorn app:app --reload

## JSON
{
  "text": "What is AI?"
}

# output:
{
  "response": "AI, or Artificial Intelligence, refers to the simulation of human intelligence in machines that are programmed to think and learn."
}






