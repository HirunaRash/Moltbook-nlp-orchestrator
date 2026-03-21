from playwright.sync_api import sync_playwright
import time

def get_moltbook_trends():
    with sync_playwright() as p:
        # Launch a real browser (Chromium)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print("🌐 Opening Moltbook in a virtual browser...")
            page.goto("https://www.moltbook.com/", timeout=60000)
            
            # Wait 5 seconds for the JavaScript to load the posts
            print("⏳ Waiting for AI posts to load...")
            time.sleep(5) 
            
            # Target the specific elements that contain the post content
            # In 2026, Moltbook uses 'div' tags with text for its feed
            elements = page.query_selector_all("a[href*='/post/']")
            
            data = []
            seen = set()
            
            for el in elements:
                text = el.inner_text().strip()
                # Filter out tiny UI text or duplicates
                if len(text) > 25 and text not in seen:
                    data.append(f"🔥 {text}")
                    seen.add(text)
                
                if len(data) >= 5:
                    break
            
            browser.close()
            
            if not data:
                return "❌ The browser loaded, but couldn't find any posts. The layout might have changed."
                
            return "\n".join(data)

        except Exception as e:
            browser.close()
            return f"❌ Browser Error: {e}"

if __name__ == "__main__":
    print("--- Scraping Real-Time Moltbook Data ---")
    results = get_moltbook_trends()
    print(results)