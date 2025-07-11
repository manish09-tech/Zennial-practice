import os
import pymupdf as fitz
from pymongo import MongoClient
from transformers import GPT2LMHeadModel, GPT2Tokenizer


MONGO_URL = "mongodb+srv://manishsaijakkula:Manishj09@news-article.jjyhq8r.mongodb.net/"
DATABASE_NAME = "resumesDB"
COLLECTION_NAME = "resumes"

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

client =MongoClient(MONGO_URL)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def load_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text=""
    for page in doc:
        text+= page.get_text()
    return text.strip()

def index_resume():
    resume_dir = "resumes"
    for filename in os.listdir(resume_dir):
        if filename.endswith(".pdf"):
            path = os.path.join(resume_dir, filename)
            text = load_pdf_text(path)
            collection.insert_one({
                "filename": filename,
                "text": text
            })
            print (f"file named: {filename} is indexed")
    return True

def query_resume(query):
    return True

# main function donot disturb
def main():
    while True:
        print ("\n GPT2 based resume query")
        print ("\n1. Process the resume in resume folder")
        print ("2. Ask query?")
        print ("3. Exit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            index_resume()
        elif choice == "2":
            query = input("Ask your query: ")
            query_resume(query)
        elif choice == "3":
            print ("Bye, see you again.")
            break
        else:
            print ("\nPlease enter correct option or try again")



if __name__ == "__main__":
    main()


