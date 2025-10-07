import requests
import re
import json
import os

# Constants
GITHUB_API = "https://api.github.com/repos/mattermost/desktop/releases/latest"
PRODUCT = "Mattermost Desktop"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/Mattermost/mattermost.json"

# Platform and architecture detection
PLATFORM_MAP = {
    "win": "Windows",
    "mac": "macOS",
    "linux": "Linux"
}

ARCH_MAP = {
    "x64": "x64",
    "amd64": "x64",
    "x86_64": "x64",
    "ia32": "x86",
    "arm64": "ARM64",
    "aarch64": "ARM64",
    "arm": "ARM"
}

SKIP_EXTENSIONS = (".blockmap", ".yml",".yml.1",".yml.2", ".json")

def detect_platform_arch(filename):
    platform = "Unknown"
    arch = "Unknown"

    for key, val in PLATFORM_MAP.items():
        if key in filename.lower():
            platform = val
            break

    for key, val in ARCH_MAP.items():
        if key in filename.lower():
            arch = val
            break

    return platform, arch

def fetch_release_assets():
    response = requests.get(GITHUB_API)
    response.raise_for_status()
    release = response.json()
    version = release["tag_name"].lstrip("v")

    results = []
    for asset in release["assets"]:
        name = asset["name"]
        url = asset["browser_download_url"]

        # Skip non-binary metadata files
        if name.lower().endswith(SKIP_EXTENSIONS):
            continue

        platform, arch = detect_platform_arch(name)

        results.append({
            "product": PRODUCT,
            "version": version,
            "file_name": name,
            "url": url,
            "platform": platform,
            "architecture": arch
        })

    return results

def save_to_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} entries to {path}")

if __name__ == "__main__":
    assets = fetch_release_assets()
    save_to_json(assets, OUTPUT_PATH)
