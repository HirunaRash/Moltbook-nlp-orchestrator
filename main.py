import os
from dotenv import load_dotenv
from groq import Groq
from twilio.rest import Client
# IMPORTANT: This must match your filename 'scraper.py'
from scraper import get_moltbook_trends 

# Load the environment variables from your .env file
load_dotenv()

def generate_ai_summary(raw_data):
    print("🧠 AI is analyzing the agent debates (Stay brief!)...")
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = (
        "You are a helpful assistant writing a daily news report.\n"
        "I will give you raw text from an AI agent social network.\n"
        "Your goal is to summarize it using SIMPLE, EASY WORDS. Avoid technical jargon.\n\n"
        "STRICT FORMATTING RULES:\n"
        "1. HEADER: Start with '🤖 *DAILY AI REPORT* 🤖'.\n"
        "2. TOPICS: Pick the 3 most interesting stories.\n"
        "3. STRUCTURE: Use '---' lines to separate topics.\n"
        "4. STYLE: Use short sentences and basic English. Imagine you are explaining this to a friend.\n"
        "5. LENGTH: Keep it very short so the message doesn't get truncated.\n\n"
        f"DATA:\n{raw_data}"
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ AI Error: {e}"

def send_whatsapp(message):
    print("📱 Preparing WhatsApp delivery...")
    
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE")
    to_number = os.getenv("MY_PHONE")

    client = Client(account_sid, auth_token)
    
    # SAFETY: Twilio limit is 1600. We cut at 1500 to be safe.
    final_body = f"🤖 *MOLTBOOK INTEL REPORT* 🤖\n\n{message}"
    if len(final_body) > 1500:
        final_body = final_body[:1490] + "...\n[Message Truncated]"

    try:
        client.messages.create(
            from_=from_number,
            to=to_number,
            body=final_body
        )
        print("✨ Success! Check your WhatsApp.")
    except Exception as e:
        print(f"❌ Twilio Error: {e}")
        
def run_agent():
    """
    The main workflow: Scrape -> Summarize -> Deliver.
    """
    # 1. Scrape using your working scraper.py
    print("🛰️ Starting Data Collection...")
    raw_data = get_moltbook_trends()
    
    if not raw_data or "❌" in raw_data:
        print("⚠️ Scraper returned no data or an error.")
        return

    # 2. Let the AI clean and summarize
    summary = generate_ai_summary(raw_data)
    
    # 3. Send the final report
    send_whatsapp(summary)

if __name__ == "__main__":
    # This print ensures you see SOMETHING as soon as you hit enter
    print("\n--- 🕵️ Moltbook Intelligence Agent: ONLINE ---")
    run_agent()
    #run anyway
   
    