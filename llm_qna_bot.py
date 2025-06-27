import os
import pymupdf as fitz

CHUNK_SIZE = 40

def chunk_text(text):
    words= text.split()
    return [" ".join(words[i: i + CHUNK_SIZE]) for i in range(0, len(words), CHUNK_SIZE)]

def extract_from_pdf(pdf_path):
    pages= fitz.open(pdf_path)
    full_text= "\n".join([page.get_text() for page in pages])
    return full_text

def add_document():
    pdf_path= input ("enter pdf path here: ").strip()
    if not os.path.exists(pdf_path):
        print(f"File not found {pdf_path}")
        return
    text= extract_from_pdf(pdf_path)

    if not text:
        print ("content not found!!")
        return
    
    text_chunks = chunk_text (text)

    print (f"content: {text_chunks}")

def query():
    return True

def del_document():
    return True

def main():

    while True:
        print ("\nSelect any options : ")
        print ("1. add document to faiss index")
        print ("2. query document")
        print ("3. delete document")
        print ("4. exit")

        choice= input("\nPlease select an option (1/2/3/4) :")

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
