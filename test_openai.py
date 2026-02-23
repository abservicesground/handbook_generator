from config import Config
from openai_handler import OpenAIHandler

print(f"API Key configured: {Config.OPENAI_API_KEY[:20]}...")
print(f"Model: {Config.OPENAI_MODEL}")

handler = OpenAIHandler()
print("\nTesting API call...")

try:
    response = handler.generate_response("Say 'Hello, test successful!'", max_tokens=50)
    print(f"✅ Response: {response}")
except Exception as e:
    print(f"❌ Error: {e}")