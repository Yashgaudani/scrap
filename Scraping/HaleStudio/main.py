import requests
import re
import json
import os

# Constants
GITHUB_API = "https://api.github.com/repos/halestudio/hale/releases/latest"
PRODUCT = "Hale Studio"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/HaleStudio/halestudio.json"

# Detect platform and architecture based on filename
def detect_platform_arch(filename):
    platform = "Unknown"
    arch = "Unknown"

    if filename.endswith(".msi") or ".win32.win32" in filename or filename.endswith(".zip"):
        platform = "Windows"
    elif "linux" in filename:
        platform = "Linux"
    elif "macosx" in filename or filename.endswith(".dmg"):
        platform = "macOS"

    if "x86_64" in filename or "x64" in filename:
        arch = "x64"
    elif "arm64" in filename:
        arch = "ARM64"
    elif "noarch" in filename:
        arch = "None"

    return platform, arch

# Fetch latest release from GitHub API
response = requests.get(GITHUB_API)
release = response.json()
version = release["tag_name"].lstrip("v")

entries = []

# Build metadata for each asset
for asset in release.get("assets", []):
    file_name = asset["name"]
    download_url = asset["browser_download_url"]
    platform, arch = detect_platform_arch(file_name)

    # Skip documentation files or Infocenter if needed
    if "infocenter" in file_name.lower():
        continue

    entries.append({
        "product": PRODUCT,
        "version": version,
        "file_name": file_name,
        "url": download_url,
        "platform": platform,
        "architecture": arch
    })

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Write to JSON file
with open(OUTPUT_PATH, "w") as f:
    json.dump(entries, f, indent=2)

print(f"Saved {len(entries)} entries to {OUTPUT_PATH}")
