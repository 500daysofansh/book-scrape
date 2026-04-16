import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_book_insights(description):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Required by OpenRouter for some free models
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000", # Required: Your site URL
        "X-OpenRouter-Title": "Book Intel Platform" # Optional: Your app name
    }
    
    prompt = f"Summarize this book in 1 sentence and give it a 1-word genre. Format as JSON: {{'summary': '...', 'genre': '...'}}. Description: {description}"
    
    payload = {
        "model": "openrouter/free", # Use the 'free' auto-router for reliability
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        # If we get a 404/400, print the actual reason from OpenRouter
        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return {"summary": "Summary unavailable", "genre": "General"}

        content = response.json()['choices'][0]['message']['content']
        # Extract JSON from potential AI markdown
        if "{" in content:
            content = content[content.find("{"):content.rfind("}")+1]
        return json.loads(content)
        
    except Exception as e:
        print(f"❌ Processing Error: {e}")
        return {"summary": "Summary unavailable", "genre": "General"}