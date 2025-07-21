import requests
import json
import os

# GitHub API URL for the latest release
API_URL = "https://api.github.com/repos/DaxStudio/DaxStudio/releases/latest"
PRODUCT_NAME = "DAX Studio"

# Destination JSON file path
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/dax_studio/daxstudio_latest.json"

# File extension to platform mapping
EXTENSION_PLATFORM_MAP = {
    ".exe": "Windows",
    ".msi": "Windows",
    ".dmg": "macOS",
    ".pkg": "macOS",
    ".deb": "Linux",
    ".rpm": "Linux",
    ".AppImage": "Linux",
    ".zip": "Cross-platform",
    ".tar.gz": "Cross-platform"
}

# Get release data
response = requests.get(API_URL)
response.raise_for_status()
data = response.json()
version = data.get("tag_name", "").lstrip("v")
assets = data.get("assets", [])

# Build results
result = []

for asset in assets:
    file_name = asset.get("name", "")
    download_url = asset.get("browser_download_url", "")
    ext = ".tar.gz" if file_name.endswith(".tar.gz") else os.path.splitext(file_name)[1]

    platform = EXTENSION_PLATFORM_MAP.get(ext)
    if not platform:
        continue  # Skip unknown types

    result.append({
        "product": PRODUCT_NAME,
        "version": version,
        "text": f"Download for {platform} – {ext.lstrip('.').upper()}",
        "url": download_url,
        "platform": platform
    })

# Save to JSON file
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(result, f, indent=2)

print(f"✅ JSON data saved to: {OUTPUT_PATH}")
