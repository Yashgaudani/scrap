import requests
from bs4 import BeautifulSoup
import os
import json
import re

# Base URL and page
base_url = "https://www.techsmith.com"
page_url = f"{base_url}/snagit/download/download-snagit-windows/"
headers = {"User-Agent": "Mozilla/5.0"}

# Target save path
save_path = "/home/yash-gaudani/R%D/patch/Scraping/snagit/snagit_links.json"

# Fetch page
response = requests.get(page_url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    data = []

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.endswith(".exe") or href.endswith(".dmg"):
            full_url = href if href.startswith("http") else base_url + href
            filename = os.path.basename(full_url)
            text = link.get_text(strip=True) or filename

            # Extract version using regex
            match = re.search(r'(\d+\.\d+\.\d+)', filename)
            version = match.group(1) if match else "unknown"

            # Detect platform
            platform = "Windows" if ".exe" in href else "macOS"

            # Add entry
            data.append({
                "product": "snagit",
                "version": version,
                "text": filename,
                "url": full_url,
                "platform": platform
            })

    # Save to JSON
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ Data saved to {save_path}")
else:
    print(f"❌ Failed to fetch page. Status code: {response.status_code}")
