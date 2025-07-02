import requests
import json
import os

BASE_URL = "https://api.github.com/repos/pbatard/rufus/releases/latest"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/Rufus/rufus_latest_api.json"

# Map file extensions or keywords to platforms
EXTENSION_PLATFORM_MAP = {
    'exe': 'Windows',
    'zip': 'Windows',
    'sig': 'Signature File',
    'txt': 'Generic',
    'sha256': 'Checksum',
    'pdb': 'Debug Symbols'
}

def detect_platform(file_name):
    ext = file_name.lower().split('.')[-1]
    
    # Handle special case like .exe.sig
    if file_name.endswith(".exe.sig"):
        return "Windows (Signature File)", "exe.sig"

    return EXTENSION_PLATFORM_MAP.get(ext, "Unknown"), ext

def fetch_latest_rufus():
    response = requests.get(BASE_URL)
    response.raise_for_status()
    release_data = response.json()

    version = release_data.get("tag_name", "unknown").lstrip("v")
    assets = release_data.get("assets", [])

    result = []
    for asset in assets:
        file_name = asset.get("name")
        download_url = asset.get("browser_download_url")

        platform, file_type = detect_platform(file_name)

        result.append({
            "product": "Rufus",
            "version": version,
            "file_name": file_name,
            "file_type": file_type,
            "url": download_url,
            "platform": platform
        })

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"✅ Saved {len(result)} Rufus download links to {OUTPUT_PATH}")

if __name__ == "__main__":
    fetch_latest_rufus()
