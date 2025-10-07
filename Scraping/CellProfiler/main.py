import requests
import os
import json
import re

# Constants
API_URL = "https://api.github.com/repos/CellProfiler/CellProfiler/releases/latest"
PRODUCT = "CellProfiler"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/CellProfiler/cellprofiler.json"

# Platform mapping based on filename
def detect_platform(filename):
    if "Windows" in filename:
        return "Windows", "x64"
    elif "macOS" in filename:
        return "macOS", "x64"
    elif filename.endswith(".AppImage") or filename.endswith(".tar.gz"):
        return "Linux", "x64"
    else:
        return None, None

def main():
    response = requests.get(API_URL)
    response.raise_for_status()
    release = response.json()
    version = release["tag_name"].lstrip("v")

    assets = release.get("assets", [])
    results = []

    for asset in assets:
        name = asset["name"]
        download_url = asset["browser_download_url"]
        platform, architecture = detect_platform(name)

        if platform:
            results.append({
                "product": PRODUCT,
                "version": version,
                "file_name": name,
                "url": download_url,
                "platform": platform,
                "architecture": architecture
            })

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Data saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
