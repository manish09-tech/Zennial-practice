import os
import pymupdf as fitz
import numpy as np


def add_document():
    return True

def query():
    return True

def del_document():
    return True

def main():

    while True:
        print ("\nSelect any options : ")
        print ("1. add document to faiss index")
        print ("2.query document")
        print ("3. delete document")
        print ("4. exit")

        choice= input("Please select an option (1/2/3/4) :")

        if choice=="1":
            add_document()
        elif choice=="2":
            query()
        elif choice=="3":
            del_document()
        elif choice=="4":
            print("Thank you!!")
            break
        else:
            print ("Incorrect choice!! Please try again....")
        
            
if __name__ == "__main__":
    main()
