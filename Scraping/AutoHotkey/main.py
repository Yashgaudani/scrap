import requests
import json
import os

API_URL = "https://api.github.com/repos/AutoHotkey/AutoHotkey/releases/latest"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/AutoHotkey/autohotkey_releases.json"

def infer_platform_and_architecture(filename):
    name = filename.lower()
    platform = "Windows" if any(ext in name for ext in [".exe", ".zip"]) else "unknown"
    architecture = "x64" if "64" in name else ("x86" if "32" in name else "unknown")
    return platform, architecture

def fetch_autohotkey_releases():
    response = requests.get(API_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch release info: {response.status_code}")

    release = response.json()
    version = release.get("tag_name", "unknown")
    product = "AutoHotkey"
    results = []

    for asset in release.get("assets", []):
        file_name = asset["name"]
        url = asset["browser_download_url"]
        platform, arch = infer_platform_and_architecture(file_name)

        results.append({
            "product": product,
            "version": version,
            "file_name": file_name,
            "url": url,
            "platform": platform,
            "architecture": arch
        })

    return results

def save_to_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ JSON saved to: {path}")

if __name__ == "__main__":
    data = fetch_autohotkey_releases()
    save_to_json(data, OUTPUT_PATH)
