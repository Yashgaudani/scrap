import requests
from bs4 import BeautifulSoup
import re
import json
import urllib.parse
from pathlib import Path

def scrape_mobaxterm():
    """Scrape MobaXterm download information."""
    print("🔍 Fetching MobaXterm download information...")
    
    # Step 1: Access Base Page
    BASE_URL = "https://mobaxterm.mobatek.net/download-home-edition.html"
    
    try:
        # Step 2: Fetch Page Content
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Step 3: Scan for Links Ending with .zip, .exe, .msi
        links = soup.find_all("a", href=True)
        results = []
        
        for link in links:
            href = link["href"]
            if href.endswith((".zip", ".exe", ".msi")) and "MobaXterm_Portable_v" in href:
                # Step 4: Parse version from filename
                file_name = href.split("/")[-1]
                match = re.search(r"MobaXterm_Portable_v(\d+(?:\.\d+)*)\.zip", file_name)
                if match:
                    version = match.group(1)
                    download_url = urllib.parse.urljoin(BASE_URL, href)
        
                    results.append({
                        "product": "MobaXterm",
                        "file_name": file_name,
                        "version": version,
                        "text": file_name,
                        "url": download_url,
                        "platform": "Windows"
                    })
        
        # Save to the expected location for the orchestrator
        output_path = Path(__file__).parent.parent / "mobaxterm_info.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {len(results)} MobaXterm entries saved to: {output_path}")
        return results
        
    except Exception as e:
        print(f"❌ Error fetching MobaXterm data: {e}")
        return []

def main():
    """Main function for standalone execution."""
    try:
        scrape_mobaxterm()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
