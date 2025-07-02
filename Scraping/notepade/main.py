import requests
import json
import os

API_URL = "https://api.github.com/repos/notepad-plus-plus/notepad-plus-plus/releases/latest"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/notepade/notepadpp_downloads.json"

def extract_architecture(filename):
    if 'x64' in filename:
        return 'x64'
    elif 'arm64' in filename.lower():
        return 'ARM64'
    elif 'x86' in filename.lower():
        return 'x86'
    else:
        return '32-bit'

def build_json(asset, version):
    filename = asset['name']
    url = asset['browser_download_url']

    return {
        "product": "Notepad++",
        "version": version,
        "text": filename,
        "url": url,
        "platform": "Windows",
        "architecture": extract_architecture(filename),
        "file_type": "exe"
    }

def main():
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()

    version = data.get("tag_name", "").lstrip('v')
    assets = data.get("assets", [])

    exe_assets = [asset for asset in assets if asset['name'].lower().endswith('.exe')]

    results = [build_json(asset, version) for asset in exe_assets]

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=4)

    print(f"✅ Saved {len(results)} .exe entries to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
