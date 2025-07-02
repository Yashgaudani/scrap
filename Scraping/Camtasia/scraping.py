import requests
from bs4 import BeautifulSoup
import json
import os

# ------------------------ Configuration ------------------------
download_page_url = "https://www.techsmith.com/camtasia/download/download-camtasia-mac/"
version_history_url = "https://support.techsmith.com/hc/en-us/articles/35532287170189-Camtasia-2025-Version-History"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
output_path = "/home/yash-gaudani/R%D/patch/Scraping/Camtasia/camtasia_links.json"

# ------------------------ Step 1: Get Latest Version ------------------------
# ------------------------ Step 1: Get Latest Version ------------------------
version_resp = requests.get(version_history_url, headers=headers)
version_resp.raise_for_status()
version_soup = BeautifulSoup(version_resp.text, "html.parser")

version = None
for h2 in version_soup.find_all("h2"):
    text = h2.get_text(strip=True)
    if "What's New in" in text and "2025." in text:
        # Example: "What's New in 2025.1.3 (25 June 2025)"
        parts = text.split("What's New in")[-1].split()
        for part in parts:
            if part.startswith("2025."):
                version = part.strip()
                break
    if version:
        break

if not version:
    version = "Unknown"



# ------------------------ Step 2: Scrape Download Links ------------------------
resp = requests.get(download_page_url, headers=headers)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

downloads = []
seen_links = set()

for a in soup.find_all("a", href=True):
    href = a['href']
    if (href.endswith(".dmg") or href.endswith(".exe")) and href not in seen_links:
        seen_links.add(href)
        file_type = href.split('.')[-1].upper()
        os_name = "macOS" if file_type == "DMG" else "Windows"
        downloads.append({
            "version": version,
            "os_name": os_name,
            "architecture": "x64",
            "edition": "Professional",
            "download_type": file_type,
            "download_link": href
        })

# ------------------------ Step 3: Save to JSON ------------------------
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w") as f:
    json.dump(downloads, f, indent=4)

print(f"✅ Saved {len(downloads)} unique links to {output_path}")
