import requests
import os
import json
import re

# Constants
GITHUB_API = "https://api.github.com/repos/cloudflare/cloudflared/releases/latest"
PRODUCT = "Cloudflared"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/cloudflared/cloudflared.json"

# Platform/Arch detection from filename
def detect_platform_arch(filename):
    platform = "Unknown"
    arch = "Unknown"

    # Normalize filename
    lower = filename.lower()

    # Platform detection
    if "windows" in lower:
        platform = "Windows"
    elif "darwin" in lower or filename.endswith(".pkg"):
        platform = "macOS"
    elif "linux" in lower:
        platform = "Linux"
    elif "freebsd" in lower:
        platform = "FreeBSD"

    # Architecture detection
    if any(x in lower for x in ["amd64", "x86_64"]):
        arch = "x86_64"
    elif "386" in lower:
        arch = "x86"
    elif "arm64" in lower or "aarch64" in lower:
        arch = "arm64"
    elif "armhf" in lower:
        arch = "armhf"
    elif "arm" in lower:
        arch = "arm"

    return platform, arch

# Fetch latest release info
response = requests.get(GITHUB_API)
release = response.json()
version = release["tag_name"]
assets = release.get("assets", [])

# Prepare data
result = []

for asset in assets:
    file_name = asset["name"]
    download_url = asset["browser_download_url"]
    platform, architecture = detect_platform_arch(file_name)

    result.append({
        "product": PRODUCT,
        "version": version,
        "file_name": file_name,
        "url": download_url,
        "platform": platform,
        "architecture": architecture
    })

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Write to JSON file
with open(OUTPUT_PATH, "w") as f:
    json.dump(result, f, indent=2)

print(f"Saved {len(result)} entries to {OUTPUT_PATH}")
