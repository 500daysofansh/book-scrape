import os
import json
import requests
from dotenv import load_dotenv

# Load API Key from root .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_book_insights(description):
    """
    Generates Summary, Genre, and Sentiment using AI.
    Requirement: AI-based insights & Sentiment Analysis.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000", # Required for OpenRouter
        "X-OpenRouter-Title": "Book Intelligence Platform"
    }
    
    # Prompting for multiple outputs in a single structured JSON response
    prompt = f"""
    Analyze the following book description and provide:
    1. A concise 1-sentence summary.
    2. A single-word genre classification.
    3. Sentiment of the description (Positive, Neutral, or Negative).
    
    Response MUST be valid JSON:
    {{"summary": "...", "genre": "...", "sentiment": "..."}}
    
    Description: {description}
    """
    
    payload = {
        "model": "openrouter/free", # Automatically uses the best available free model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        content = response.json()['choices'][0]['message']['content']
        
        # Clean AI markdown wrapper if present
        if "{" in content:
            content = content[content.find("{"):content.rfind("}")+1]
            
        return json.loads(content)
        
    except Exception as e:
        print(f"⚠️ AI insight error: {e}")
        # Return fallback data so the scraper doesn't crash
        return {
            "summary": "Summary currently unavailable.",
            "genre": "General",
            "sentiment": "Neutral"
        }