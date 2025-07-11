import os
import faiss
import numpy as np
import fitz

from openai import OpenAI
from pymongo import MongoClient

PDF = "resumes"
FAISS_INDEX = "resume_index.faiss"
INDEX_DATA = "resume_chunks.py"
MONGO_URL = "mongodb+srv://manishsaijakkula:Manishj09@news-article.jjyhq8r.mongodb.net/"
DATABASE_NAME = ""
COLLECTION_NAME = ""

def load_pdf_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    return "\n".join({page.get_text() for page in pdf_document})

def index_resume():
    return True

def query_resume(query):
    return True

def main():
    while True:
        print ("\n GPT4 based resume query")
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



