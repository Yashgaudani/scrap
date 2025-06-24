import requests
from bs4 import BeautifulSoup
import re
import json
import os

# Base URL
url = "https://www.oracle.com/virtualization/technologies/vm/downloads/virtualbox-downloads.html"
headers = {"User-Agent": "Mozilla/5.0"}

# Output file path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/OracleVM/virtualbox_downloads.json"

# Patterns
file_exts = (".exe", ".dmg", ".rpm", ".deb", ".msi", ".zip", ".tar.gz")
platform_keywords = {
    "Windows": ["win", "windows"],
    "macOS": ["osx", "mac"],
    "Linux": ["linux", "rpm", "deb"]
}

def detect_platform(url):
    for platform, keywords in platform_keywords.items():
        if any(k in url.lower() for k in keywords):
            return platform
    return "Unknown"

def extract_version_from_url(url):
    match = re.search(r"/virtualbox/([\d.]+)/", url)
    return match.group(1) if match else "unknown"

# Fetch HTML
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Extract download data
results = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    text = a.get_text(strip=True)

    if any(href.lower().endswith(ext) for ext in file_exts):
        full_url = href if href.startswith("http") else "https:" + href
        version = extract_version_from_url(full_url)
        platform = detect_platform(full_url)

        results.append({
            "product": "VirtualBox",
            "version": version,
            "text": text,
            "url": full_url,
            "platform": platform
        })

# Ensure directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save to JSON file
with open(output_path, "w") as f:
    json.dump(results, f, indent=4)

print(f"✅ Data saved to {output_path}")
