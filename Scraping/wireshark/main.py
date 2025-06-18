import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

def scrape_wireshark():
    """Scrape Wireshark download information."""
    print("🔍 Fetching Wireshark download information...")
    
    # Base URL
    url = "https://2.na.dl.wireshark.org/"
    
    try:
        # Fetch the page
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Get raw HTML
        html_content = response.text
        
        # Parse for download links
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Find download links (this is a basic implementation)
        download_links = []
        
        # Look for common Wireshark download patterns
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text(strip=True)
            
            # Filter for Wireshark installers
            if any(ext in href.lower() for ext in ['.exe', '.dmg', '.deb', '.rpm', '.tar.gz']):
                if 'wireshark' in href.lower():
                    download_links.append({
                        "product": "wireshark",
                        "version": "latest",  # Version extraction would need more parsing
                        "text": text or "Wireshark Download",
                        "url": url + href if href.startswith('/') else href,
                        "platform": "Unknown"
                    })
        
        # If no specific links found, create a basic structure
        if not download_links:
            download_links = [{
                "product": "wireshark",
                "version": "latest",
                "text": "Wireshark Download",
                "url": "https://www.wireshark.org/download.html",
                "platform": "Multiple"
            }]
        
        # Save to the expected location for the orchestrator
        output_path = Path(__file__).parent.parent / "wireshark_info.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(download_links, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Wireshark data saved to: {output_path}")
        return download_links
        
    except Exception as e:
        print(f"❌ Error fetching Wireshark data: {e}")
        return []

def main():
    """Main function for standalone execution."""
    try:
        scrape_wireshark()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
