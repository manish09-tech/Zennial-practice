import json
import logging
from datetime import datetime
from functools import wraps

logging.basicConfig(
    filename='bookstore_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"Executing: {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Error while Executing: {func.__name__} : {e}")
    return wrapper

class Book:
    def __init__(self, book_id, title, author, genre, price, published_date, stock):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price
        self.published_date = published_date
        self.stock = stock

    def is_in_stock(self):
        return self.stock > 0

# ***** Helper Methods *****
@handle_exceptions
def load_books(filepath):
    with open(filepath, 'r') as f:
        books = json.load(f)
        return [Book(**b) for b in books]

def showcli():
    while True:
        print("\n ===== Book Store Menu =====")
        print("1. List All Books")
        print("2. Find All Books In Stock")
        print("3. Exit")

        choice = input("Please Select an Option : ")

        if choice == "1":
            for book in books:
                print(f"{book.book_id} - {book.title} by {book.author} - {book.genre} - ${book.price} - Published: {book.published_date} - Stock: {book.stock}")

        elif choice == "2":
            for book in books:
                if book.is_in_stock():
                    print(f"{book.book_id} - {book.title} - In Stock: {book.stock}")
         
        elif choice == "3":
            print("Exiting Bookstore CLI. Thank you!")
            break
        else:
            print("Invalid Choice. Please enter a number between 1 and 3")

if __name__ == "__main__":
    filepath = "books_data.json"
    books = load_books(filepath=filepath)

    if books:
        showcli()
    else:
        print("No books found or file is missing")