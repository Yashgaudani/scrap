import requests
import os
import json

# Constants
PRODUCT = "Get_iplayer"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/get_iplayer/get_iplayer.json"
GITHUB_APIS = [
    "https://api.github.com/repos/get-iplayer/get_iplayer_win32/releases/latest",
    "https://api.github.com/repos/get-iplayer/get_iplayer_macos/releases/latest"
]

# Detect platform and architecture from filename
def detect_platform_arch(filename):
    platform = "Unknown"
    arch = "Unknown"
    name = filename.lower()

    if "windows" in name:
        platform = "Windows"
    elif "macos" in name or filename.endswith(".pkg"):
        platform = "macOS"

    if "x64" in name or "x86_64" in name:
        arch = "x86_64"
    elif "x86" in name and "x64" not in name:
        arch = "x86"

    return platform, arch

# Collect all assets from both sources
result = []

for api_url in GITHUB_APIS:
    response = requests.get(api_url)
    release = response.json()
    version = release.get("tag_name", "").lstrip("v")
    assets = release.get("assets", [])

    for asset in assets:
        filename = asset["name"]

        # Include only installer files, exclude hash/checksum files
        if filename.endswith((".exe", ".pkg")):
            url = asset["browser_download_url"]
            platform, arch = detect_platform_arch(filename)

            result.append({
                "product": PRODUCT,
                "version": version,
                "file_name": filename,
                "url": url,
                "platform": platform,
                "architecture": arch
            })

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Save JSON
with open(OUTPUT_PATH, "w") as f:
    json.dump(result, f, indent=2)

print(f"Saved {len(result)} entries to {OUTPUT_PATH}")
