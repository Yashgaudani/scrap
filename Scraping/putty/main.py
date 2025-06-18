import requests
from bs4 import BeautifulSoup
import json
import os
import re
from pathlib import Path

def scrape_putty():
    """Scrape PuTTY download information."""
    print("🔍 Fetching PuTTY download information...")
    
    url = "https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html"
    base_url = "https://www.chiark.greenend.org.uk/~sgtatham/putty/"

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        result = []

        # Extract all .msi download links
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.endswith('.msi') and 'installer' in href:
                filename = href.split('/')[-1]
                full_url = base_url + filename

                # Extract version from filename
                version_match = re.search(r'putty.*?([0-9]+\.[0-9]+).*?installer\.msi', filename)
                version = version_match.group(1) if version_match else "unknown"

                # Detect architecture
                if "64bit" in filename:
                    arch = "64-bit x86"
                elif "arm64" in filename:
                    arch = "64-bit Arm"
                elif re.match(r'putty-\d+\.\d+-installer\.msi', filename) or "putty-0" in filename:
                    arch = "32-bit x86"
                else:
                    arch = "unknown"

                result.append({
                    "product": "putty",
                    "version": version,
                    "text": filename,
                    "url": full_url,
                    "platform": "Windows"
                })

        # Save to the expected location for the orchestrator
        output_path = Path("/home/yash-gaudani/R%D/patch/Scraping/putty/putty_info.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved {len(result)} MSI links to: {output_path}")
        return result
        
    except Exception as e:
        print(f"❌ Error fetching PuTTY data: {e}")
        return []

def main():
    """Main function for standalone execution."""
    try:
        scrape_putty()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
