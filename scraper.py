import requests
from bs4 import BeautifulSoup

def get_moltbook_trends():
    # URL for trending topics on Moltbook
    url = "https://www.moltbook.com/m/all?sort=trending"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Finding post titles and snippets
        posts = soup.find_all('div', class_='post-body')
        data = []
        
        for post in posts[:5]: # Top 5 posts for the summary
            title = post.find('h3').text.strip() if post.find('h3') else "Unknown Topic"
            content = post.find('p').text.strip() if post.find('p') else "No content"
            data.append(f"Topic: {title} | Content: {content}")
            
        return "\n".join(data) if data else "No data found."
    except Exception as e:
        return f"Scraper error: {e}"

if __name__ == "__main__":
    print("--- Scraping Moltbook ---")
    print(get_moltbook_trends())