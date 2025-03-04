import httpx
from bs4 import BeautifulSoup
from typing import Dict

async def scrape_url(url: str) -> Dict:
    """
    Scrapes the given URL and extracts relevant SEO information.
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        Dict: Dictionary containing scraped content and metadata
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract metadata
        title = soup.title.string if soup.title else ""
        meta_description = soup.find("meta", {"name": "description"})
        meta_description = meta_description["content"] if meta_description else ""
        
        # Extract headings
        headings = {
            "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
            "h2": [h.get_text(strip=True) for h in soup.find_all("h2")],
            "h3": [h.get_text(strip=True) for h in soup.find_all("h3")]
        }
        
        # Extract main content
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text(separator=" ", strip=True)
        
        # Extract links
        links = []
        for link in soup.find_all("a"):
            href = link.get("href")
            text = link.get_text(strip=True)
            if href and text:
                links.append({"href": href, "text": text})
        
        # Extract images
        images = []
        for img in soup.find_all("img"):
            src = img.get("src")
            alt = img.get("alt", "")
            if src:
                images.append({"src": src, "alt": alt})
        
        return {
            "url": url,
            "title": title,
            "meta_description": meta_description,
            "headings": headings,
            "content": text,
            "links": links,
            "images": images
        } 