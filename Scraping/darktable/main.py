import requests
import re
import json
import os

# GitHub API for latest release
API_URL = "https://api.github.com/repos/darktable-org/darktable/releases/latest"

# Output path
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/darktable/darktable_releases.json"

# Patterns to detect platform and architecture
platform_arch_map = [
    (r'win64\.exe$', 'Windows', 'x64'),
    (r'arm64.*\.dmg$', 'macOS', 'arm64'),
    (r'x86_64.*\.dmg$', 'macOS', 'x64'),
    (r'x86_64\.AppImage$', 'Linux', 'x64'),
    (r'arm64.*\.AppImage$', 'Linux', 'arm64'),
    (r'\.tar\.xz$', 'Linux', 'source')
]

def infer_platform_arch(filename):
    for pattern, platform, arch in platform_arch_map:
        if re.search(pattern, filename, re.IGNORECASE):
            return platform, arch
    return "Unknown", "Unknown"

def fetch_darktable_assets():
    response = requests.get(API_URL)
    response.raise_for_status()
    release_data = response.json()

    version = release_data['tag_name'].lstrip("v")
    assets = release_data.get("assets", [])
    
    output = []

    for asset in assets:
        file_name = asset.get("name")
        download_url = asset.get("browser_download_url")
        platform, arch = infer_platform_arch(file_name)

        if platform != "Unknown":
            output.append({
                "product": "Darktable",
                "version": version,
                "file_name": file_name,
                "url": download_url,
                "platform": platform,
                "architecture": arch
            })

    return output

# Main block to fetch and write JSON
if __name__ == "__main__":
    try:
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        data = fetch_darktable_assets()
        with open(OUTPUT_PATH, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ JSON saved to: {OUTPUT_PATH}")
    except Exception as e:
        print(f"❌ Error: {e}")
