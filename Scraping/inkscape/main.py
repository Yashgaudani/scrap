import requests
from bs4 import BeautifulSoup
import os
import re
import json

BASE_URL = "https://inkscape.org"
TARGET_URL = f"{BASE_URL}/release/1.4.2/platforms/"
OUTPUT_FILE = "/home/yash-gaudani/R%D/patch/Scraping/inkscape/inkscape.json"

def extract_version(filename):
    match = re.search(r'[-_](\d+\.\d+\.\d+)', filename)
    if match:
        return match.group(1)
    match = re.search(r'[-_](\d+\.\d+)', filename)
    if match:
        return match.group(1)
    return "Unknown"

def detect_platform_arch(filename):
    filename = filename.lower()
    if filename.endswith(".exe") or filename.endswith(".msi") or filename.endswith(".7z"):
        platform = "Windows"
        arch = "x64" if "x64" in filename else "x86"
    elif filename.endswith(".dmg"):
        platform = "macOS"
        arch = "arm64" if "arm64" in filename else "x64"
    elif filename.endswith(".appimage"):
        platform = "Linux"
        arch = "x64" if "x86_64" in filename else "Unknown"
    elif filename.endswith(".tar.xz"):
        platform = "Linux"
        arch = "Unknown"
    else:
        platform = "Unknown"
        arch = "Unknown"
    return platform, arch

def scrape_inkscape():
    response = requests.get(TARGET_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    download_links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/gallery/item/") and not href.endswith("/download"):
            full_url = BASE_URL + href
            filename = os.path.basename(href)
            version = extract_version(filename)
            platform, arch = detect_platform_arch(filename)

            download_links.append({
                "product": "Inkscape",
                "version": version,
                "file_name": filename,
                "url": full_url,
                "platform": platform,
                "architecture": arch
            })

    return download_links

def save_json(data):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved {len(data)} entries to {OUTPUT_FILE}")

if __name__ == "__main__":
    try:
        data = scrape_inkscape()
        save_json(data)
    except Exception as e:
        print(f"❌ Error: {e}")
