import requests
import re
import json
import os

GITHUB_API = "https://api.github.com/repos/alacritty/alacritty/releases/latest"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/Alacritty/alacritty_releases.json"

def detect_platform_arch(filename):
    lower = filename.lower()

    if filename.endswith(".msi") or filename.endswith(".exe"):
        return "Windows", "x64"
    elif filename.endswith(".dmg"):
        return "mac", "x64"
    elif filename.endswith(".app.tar.gz"):
        return "mac", "arm64"
    elif ".deb" in lower or ".tar.gz" in lower or ".desktop" in lower:
        return "Linux", "x64"
    else:
        return "unknown", "unknown"

def fetch_alacritty_releases():
    response = requests.get(GITHUB_API)
    data = response.json()
    results = []

    tag_version = data.get("tag_name", "unknown")

    for asset in data.get("assets", []):
        file_name = asset["name"]
        download_url = asset["browser_download_url"]
        platform, arch = detect_platform_arch(file_name)

        entry = {
            "product": "Alacritty",
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
    data = fetch_alacritty_releases()
    save_to_json(data, OUTPUT_PATH)
