import os
import pymupdf as fitz
from pymongo import MongoClient
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Constants
MONGO_URL = "mongodb+srv://manishsaijakkula:Manishj09@news-article.jjyhq8r.mongodb.net/"
DATABASE_NAME = "resumesDB"
COLLECTION_NAME = "resumes"
RESUME_DIR = "resumes"
MAX_INPUT_TOKENS = 768  
CHUNK_SIZE = 700 

# Load GPT2 model & tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

# Connect to MongoDB
client = MongoClient(MONGO_URL)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Load text from PDF
def load_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

# Index all PDFs in "resumes" directory
def index_resume():
    for filename in os.listdir(RESUME_DIR):
        if filename.endswith(".pdf"):
            path = os.path.join(RESUME_DIR, filename)
            text = load_pdf_text(path)
            collection.insert_one({
                "filename": filename,
                "text": text
            })
            print(f"File named '{filename}' is indexed.")
    return True

# Chunk text into token-based chunks to avoid truncation
def chunk_text(text, chunk_size=CHUNK_SIZE):
    tokens = tokenizer.encode(text)
    for i in range(0, len(tokens), chunk_size):
        yield tokenizer.decode(tokens[i:i+chunk_size])

# Use GPT2 to generate an answer based on prompt with better parameters
def generate_answer(prompt, max_length=100):
    inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=MAX_INPUT_TOKENS)
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=inputs.shape[1] + max_length,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

# Query resumes using GPT2 over chunks and pick best answer (naive: first answer)
def query_resume(query):
    print("\nSearching resumes...\n")
    resumes = list(collection.find())
    for resume in resumes:
        resume_text = resume['text']
        best_answer = ""
        print(f"\nFrom resume: {resume['filename']}")
       
        for chunk in chunk_text(resume_text):
            prompt = f"Given the resume below:\n{chunk}\n\nAnswer this question: {query}\nAnswer:"
            answer = generate_answer(prompt)
           
            if answer and answer != query and len(answer) > 10:
                best_answer = answer
                break
        if best_answer:
            print("Answer:\n", best_answer)
        else:
            print("No meaningful answer found.")
    return True

# Main menu
def main():
    while True:
        print("\nGPT2-Based Resume Query System")
        print("1. Process resumes in the 'resumes' folder")
        print("2. Ask a query")
        print("3. Exit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            index_resume()
        elif choice == "2":
            query = input("Ask your query: ")
            query_resume(query)
        elif choice == "3":
            print("Bye, see you again.")
            break
        else:
            print("Please enter a correct option or try again.")

if __name__ == "__main__":
    main()
