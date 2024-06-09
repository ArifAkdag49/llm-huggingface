import requests
from huggingface_hub import login

# Hugging Face API token ve URL
HUGGING_FACE_API_TOKEN = "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"
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

# Hugging Face ile kimlik doğrulama
login(token=HUGGING_FACE_API_TOKEN)

def get_model_info():
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}"}
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.json()}")
    
    model_info = response.json()
    print(f"Model info:\n{model_info}\n")

if __name__ == "__main__":
    get_model_info()
