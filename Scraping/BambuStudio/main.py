import requests
import re
import json
import os

GITHUB_API = "https://api.github.com/repos/bambulab/BambuStudio/releases/latest"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/BambuStudio/bambu_studio_releases.json"

def detect_platform_arch(filename):
    lower = filename.lower()
    if "linux" in lower:
        return "Linux", "x64" if "appimage" in lower else "unknown"
    elif "mac" in lower or "darwin" in lower:
        return "mac", "arm64" if "arm" in lower else "x64"
    elif "win" in lower:
        return "Windows", "x64"
    return "unknown", "unknown"

def fetch_bambu_releases():
    response = requests.get(GITHUB_API)
    data = response.json()
    results = []

    tag_version = data.get("tag_name", "unknown")

    for asset in data.get("assets", []):
        file_name = asset["name"]
        download_url = asset["browser_download_url"]
        platform, arch = detect_platform_arch(file_name)

        entry = {
            "product": "BambuStudio",
            "version": tag_version,
            "file_name": file_name,
            "url": download_url,
            "platform": platform,
            "architecture": arch
        }

        results.append(entry)

    return results

def save_to_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Data saved to: {path}")

if __name__ == "__main__":
    data = fetch_bambu_releases()
    save_to_json(data, OUTPUT_PATH)
