import fitz # read pdf file
import os
import logging
import openai
import numpy as np
from dotenv import load_dotenv
import sys


load_dotenv()
openai.ai_key = os.getenv("OPENAI_API_KEY")

PDF_FILE_PATH = "C:\online-book-store\women.pdf"

logging.basicConfig(
    filename= "bot_cli.log",
    level=logging.INFO,
    format= "%(asctime)s-%(levelname)s-%(message)s"
)

logger = logging.getLogger(__name__)

def extract_text_from_pdf (pdf_file_path):
    try:
        pdf_pages= fitz.open(pdf_file_path)
        full_pdf_text = "\n".join([page.get_text()for page in pdf_pages])# read each page

        logger.info(f" Extracted txt from file{pdf_file_path} with the length {len(full_pdf_text)}")
    except Exception as e:
        logger.exception(f"Failed to read txt from {pdf_file_path}. ERROR is {e}")

def main():

    if not os.path.exists(PDF_FILE_PATH):
        print("source pdf not found.")
        sys.exit(1)
        

