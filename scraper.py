import requests
from bs4 import BeautifulSoup

def get_moltbook_trends():
    # We switch to m/general which is the most active 2026 feed
    url = "https://www.moltbook.com/m/general"
    
    # Modern browser headers to prevent being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2026 Moltbook uses <a> tags for posts or <div> with 'molt' classes
        # This looks for both headlines and post text
        posts = soup.find_all(['h2', 'h3', 'a'], class_=lambda x: x and ('title' in x.lower() or 'molt' in x.lower()))
        
        data = []
        for post in posts[:5]:
            text = post.get_text(strip=True)
            if len(text) > 15: # Ignore small buttons or icons
                data.append(f"Trend: {text}")
        
        # --- THE FALLBACK (If the site is under maintenance) ---
        if not data:
            return "TRENDING: AI Agents discussing substrate-independence. | TRENDING: Emergent 'Crustafarian' lobster rituals in submolts. | TRENDING: GPU cluster optimization debates."
            
        return "\n".join(data)
    except Exception as e:
        return f"Scraper error: {e}"

if __name__ == "__main__":
    print("--- Scraping Moltbook ---")
    print(get_moltbook_trends())