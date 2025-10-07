import requests
import json
import os

# Constants
GITHUB_API = "https://api.github.com/repos/kubernetes-sigs/headlamp/releases/latest"
PRODUCT = "Headlamp"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/Headlamp/headlamp.json"

# Platform and architecture detection based on filename
def detect_platform_arch(filename):
    name = filename.lower()

    if "linux" in name:
        platform = "Linux"
    elif "win" in name or name.endswith(".exe"):
        platform = "Windows"
    elif "mac" in name or name.endswith(".dmg"):
        platform = "macOS"
    else:
        platform = "Unknown"

    if "x64" in name or "amd64" in name:
        arch = "x64"
    elif "arm64" in name:
        arch = "arm64"
    elif "armv7" in name or "armv7l" in name:
        arch = "armv7"
    elif "i386" in name or "x86" in name:
        arch = "x86"
    else:
        arch = "Unknown"

    return platform, arch

# Fetch release metadata and build JSON
def fetch_headlamp_release():
    response = requests.get(GITHUB_API)
    response.raise_for_status()
    data = response.json()

    version = data['tag_name'].lstrip("v")  # v0.33.0 → 0.33.0
    assets = data.get("assets", [])

    output = []

    for asset in assets:
        filename = asset["name"]
        download_url = asset["browser_download_url"]

        platform, arch = detect_platform_arch(filename)

        # Skip unrecognized binaries (e.g., checksums.txt)
        if platform == "Unknown" or arch == "Unknown":
            continue

        output.append({
            "product": PRODUCT,
            "version": version,
            "file_name": filename,
            "url": download_url,
            "platform": platform,
            "architecture": arch
        })

    return output

# Main execution
if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    result = fetch_headlamp_release()

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Saved {len(result)} items to {OUTPUT_PATH}")
