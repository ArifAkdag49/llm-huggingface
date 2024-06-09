import os
import requests
from huggingface_hub import login
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pdf_okuma_002 import read_pdf

# Hugging Face API token ve URL
HUGGING_FACE_API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

# Hugging Face ile kimlik doğrulama
login(token=HUGGING_FACE_API_TOKEN)

app = FastAPI()

# PDF içeriğini okuma
data_directory = "./data"
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

    # PDF içeriğinde sorgunun cevabı olup olmadığını kontrol et
    if query.lower() in context.lower(): 
    
        return answer
    else:
        return "Bilgi PDF'de yok."

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
