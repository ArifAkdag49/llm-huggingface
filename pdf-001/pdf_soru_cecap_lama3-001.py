import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
from huggingface_hub import login
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import fitz  # PyMuPDF

# Hugging Face API token ve URL
HUGGING_FACE_API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

# Hugging Face ile kimlik doğrulama
login(token=HUGGING_FACE_API_TOKEN)

app = FastAPI()

def read_pdf(data_directory):
    pdf_text = ""
    for filename in os.listdir(data_directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(data_directory, filename)
            try:
                with fitz.open(file_path) as pdf:
                    for page_num in range(pdf.page_count):
                        page = pdf.load_page(page_num)
                        pdf_text += page.get_text()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    return pdf_text

data_directory = "/home/ubuntu/llm-project/data"
pdf_content = read_pdf(data_directory)

def prepare_context():
    context = pdf_content
    return context

def query_model(query):
    context = prepare_context()
    input_text = f"Context: {context}\n\nQuery: {query}"
    
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}"}
    payload = {"inputs": input_text, "parameters": {"max_length": 500}}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    
    answer = response.json()[0]['generated_text']
    return answer

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_endpoint(request: QueryRequest):
    answer = query_model(request.query)
    return {"answer": answer}

def main():
    while True:
        command = input("Komutunuzu girin (çıkmak için 'exit' yazın): ")
        if command.lower() == 'exit':
            break
        answer = query_model(command)
        print(f"Yanıt: {answer}")

if __name__ == "__main__":
    main()
