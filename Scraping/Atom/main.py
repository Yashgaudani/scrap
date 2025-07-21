import requests
import json
import os

# GitHub API for Atom latest release
API_URL = "https://api.github.com/repos/atom/atom/releases/latest"
PRODUCT_NAME = "Atom"

# Output path
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/Atom/atom_latest.json"

# File extension to fallback platform
EXTENSION_FALLBACK = {
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

# Platform detection keywords
PLATFORM_KEYWORDS = {
    "win": "Windows",
    "windows": "Windows",
    "mac": "macOS",
    "osx": "macOS",
    "linux": "Linux"
}

# Architecture detection
ARCHITECTURE_KEYWORDS = {
    "x64": "x64",
    "amd64": "x64",
    "x86": "x86",
    "386": "x86",
    "arm64": "ARM64",
    "armv7": "ARMv7"
}

# Fetch data
response = requests.get(API_URL)
response.raise_for_status()
data = response.json()

version = data.get("tag_name", "").lstrip("v")
assets = data.get("assets", [])

results = []

for asset in assets:
    original_file = asset.get("name", "")
    file_name = original_file.lower()
    url = asset.get("browser_download_url", "")

    # Detect extension
    ext = ".tar.gz" if file_name.endswith(".tar.gz") else os.path.splitext(file_name)[1]

    # Detect platform from filename
    platform = None
    for key, val in PLATFORM_KEYWORDS.items():
        if key in file_name:
            platform = val
            break

    # Fallback to extension if filename doesn't help
    if not platform:
        platform = EXTENSION_FALLBACK.get(ext, "Unknown")

    # Detect architecture
    architecture = "Unknown"
    for key, val in ARCHITECTURE_KEYWORDS.items():
        if key in file_name:
            architecture = val
            break

    results.append({
        "product": PRODUCT_NAME,
        "version": version,
        "file_name": original_file,
        "url": url,
        "platform": platform,
        "architecture": architecture
    })

# Save output
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ Atom release JSON saved to: {OUTPUT_PATH}")
