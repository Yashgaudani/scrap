import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import json
import os

# Base URL
base_url = "https://www.archimatetool.com/download/"

# Output path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/archi/archi_downloads.json"

# Regex for download links
download_regex = re.compile(r'.*\.(exe|zip|tar\.gz|tgz|dmg|sh)$', re.IGNORECASE)

# Detect platform
def detect_platform(text):
    text = text.lower()
    if "win" in text or text.endswith((".exe", ".zip")):
        return "windows"
    elif "mac" in text or text.endswith(".dmg"):
        return "macos"
    elif "linux" in text or text.endswith((".tar.gz", ".tgz", ".sh")):
        return "linux"
    return "unknown"

# Detect architecture
def detect_architecture(text, platform):
    text = text.lower()
    if "win64" in text:
        return "x64"
    elif "silicon" in text:
        return "arm64"
    elif platform == "macos":
        return "intel"
    else:
        return "x64"  # default

# Extract version
def extract_version(text):
    match = re.search(r'(\d+\.\d+(?:\.\d+)*)', text)
    return match.group(1) if match else ""

# Main scraper
response = requests.get(base_url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

results = []

for a in soup.find_all("a", href=True):
    href = a["href"].strip()
    if download_regex.match(href):
        full_url = urljoin(base_url, href)
        filename = href.split("/")[-1]

        platform = detect_platform(filename)
        architecture = detect_architecture(filename, platform)
        version = extract_version(filename)

        results.append({
            "product": "archi",
            "version": version,
            "text": filename,
            "url": full_url,
            "platform": platform,
            "architecture": architecture
        })

# Ensure output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save as JSON
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"Saved {len(results)} entries to {output_path}")
