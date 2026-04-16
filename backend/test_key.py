import os
from dotenv import load_dotenv

print("🔍 1. Looking for .env file...")
load_dotenv()

key = os.getenv("OPENROUTER_API_KEY")

if key:
    print(f"✅ 2. Key found in .env: {key[:10]}...")
else:
    print("❌ 2. Key NOT found. Check your .env file naming and location.")
    print(f"   Current Directory: {os.getcwd()}")
    exit()

print("🌐 3. Testing connection to OpenRouter...")
import requests
try:
    response = requests.get(
        "https://openrouter.ai/api/v1/auth/key", 
        headers={"Authorization": f"Bearer {key}"}
    )
    print(f"📊 4. API Response Code: {response.status_code}")
    print(f"💬 5. API Body: {response.json()}")
except Exception as e:
    print(f"❌ 6. Connection Error: {e}")