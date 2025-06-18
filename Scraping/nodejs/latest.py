import requests
from bs4 import BeautifulSoup
import os
import json
import re

BASE_URL = "https://nodejs.org/dist/"
SAVE_PATH = "/home/yash-gaudani/R%D/Vlc/nodejs/nodejs.json"

def detect_platform(filename):
    fname = filename.lower()

    if "aix" in fname:
        return "AIX"
    elif "sunos" in fname:
        return "SunOS"
    elif "darwin" in fname or "mac" in fname:
        return "macOS"
    elif "linux" in fname:
        return "Linux"
    elif "win" in fname:
        return "Windows"
    elif fname.endswith(".pkg"):
        return "macOS"
    elif fname.endswith(".msi") or fname.endswith(".exe"):
        return "Windows"
    else:
        return "Unknown"

def extract_version(filename):
    match = re.search(r'node-v(\d+\.\d+\.\d+)', filename)
    return match.group(1) if match else "unknown"

def get_latest_url():
    response = requests.get(BASE_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all('a'):
        href = link.get("href", "")
        if href.strip("/") == "latest":
            return BASE_URL + href
    raise Exception("latest/ directory not found")

def scrape_latest_nodejs_files(latest_url):
    response = requests.get(latest_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    result = []
    skip_exts = (".txt", ".asc", ".sig", ".json")
    
    for link in soup.find_all("a"):
        href = link.get("href", "")
        if not href or href.endswith("/") or href.endswith(skip_exts):
            continue

        filename = os.path.basename(href)
        full_url = latest_url + filename
        version = extract_version(filename)
        platform = detect_platform(filename)

        result.append({
            "product": "Node.js",
            "version": version,
            "text": filename,
            "url": full_url,
            "platform": platform
        })

    return result

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Saved JSON to: {path}")

# Run
if __name__ == "__main__":
    latest_url = get_latest_url()
    data = scrape_latest_nodejs_files(latest_url)
    save_json(data, SAVE_PATH)
