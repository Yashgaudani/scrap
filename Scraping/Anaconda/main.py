import requests
from bs4 import BeautifulSoup
import re
from packaging.version import Version
import json
import os

# Base URL and output file
BASE_URL = "https://repo.anaconda.com/archive"
OUTPUT_JSON = "/home/yash-gaudani/R%D/patch/Scraping/Anaconda/anaconda_latest.json"

# File types to include
FILE_TYPES = [".exe", ".pkg", ".sh"]

# Regex to extract version and platform info
pattern = re.compile(r"Anaconda3-(\d{4}\.\d{2}-\d+)-(Windows|MacOSX|Linux)-(x86_64|arm64)\.(exe|pkg|sh)")

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

files = []

for link in soup.find_all("a", href=True):
    href = link["href"]
    if any(href.endswith(ft) for ft in FILE_TYPES):
        match = pattern.search(href)
        if match:
            version_str, os_name, arch, ext = match.groups()
            files.append({
                "file_name": href,
                "version": version_str,
                "os": os_name,
                "architecture": arch,
                "file_type": ext,
                "url": f"{BASE_URL}/{href}"
            })

# Get latest version
def parse_version(vstr):
    return Version(vstr.split('-')[0])

latest_version = max(files, key=lambda x: parse_version(x["version"]))["version"]

# Filter only latest version files
latest_files = [f for f in files if f["version"] == latest_version]

# Save to JSON file
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
with open(OUTPUT_JSON, "w") as f:
    json.dump(latest_files, f, indent=4)

print(f"Saved {len(latest_files)} latest Anaconda files to {OUTPUT_JSON}")