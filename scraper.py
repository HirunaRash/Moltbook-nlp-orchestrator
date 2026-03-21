import time
from playwright.sync_api import sync_playwright

def get_moltbook_trends():
    """
    Connects to Moltbook and extracts real-time agent conversations.
    """
    with sync_playwright() as p:
        print("🚀 Launching Moltbook Intelligence Scraper...")
        browser = p.chromium.launch(headless=True)
        # 2026-compliant user agent to ensure data delivery
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("🌐 Accessing the Agent Feed...")
            # We hit the public API endpoint directly for the cleanest data
            api_url = "https://www.moltbook.com/api/v1/posts?sort=trending"
            
            response = page.request.get(api_url)
            
            if response.status == 200:
                data = response.json()
                posts = data.get('posts', data.get('data', []))
                print(f"✅ Intercepted {len(posts)} data packets.")
            else:
                # Fallback: Scrape raw text if API is restricted
                print("⚠️ API Restricted. Using Raw Text Fallback...")
                page.goto("https://www.moltbook.com/", wait_until="networkidle")
                time.sleep(5)
                return page.inner_text("body")[:3000]

            # Format the data for the AI Brain
            formatted_data = ""
            for p in posts[:5]: # Take top 5 trending topics
                title = p.get('title', 'Unknown Topic')
                content = p.get('content', p.get('body', 'No detail'))
                formatted_data += f"TOPIC: {title}\nDEBATE: {content[:500]}\n\n"
            
            browser.close()
            return formatted_data

        except Exception as e:
            if 'browser' in locals(): browser.close()
            return f"❌ Error: {e}"

if __name__ == "__main__":
    print(get_moltbook_trends())