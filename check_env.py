import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def run_health_check():
    print("🔍 --- System Health Check ---")
    
    # Check .env variables
    keys = ["GROQ_API_KEY", "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN"]
    for key in keys:
        if os.getenv(key):
            print(f"✅ {key} is configured.")
        else:
            print(f"❌ {key} is MISSING in .env!")

    # Test Groq Connection
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5
        )
        print("✅ Groq AI: Connection Successful.")
    except Exception as e:
        print(f"❌ Groq AI: Connection Failed ({e})")

if __name__ == "__main__":
    run_health_check()
    #chech api health