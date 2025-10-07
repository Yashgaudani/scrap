import requests
import re
import json
import os

# Constants
GITHUB_API = "https://api.github.com/repos/frostwire/frostwire/releases/latest"
PRODUCT = "FrostWire"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/frostwire/frostwire.json"

def detect_platform_arch(filename):
    platform = "Unknown"
    arch = "Unknown"

    if filename.endswith(".exe"):
        platform = "Windows"
        arch = "x64"
    elif filename.endswith(".dmg"):
        platform = "macOS"
        if "arm64" in filename:
            arch = "arm64"
        elif "x86_64" in filename:
            arch = "x64"
    elif filename.endswith(".deb") or filename.endswith(".tar.gz"):
        platform = "Linux"
        if "amd64" in filename:
            arch = "x64"
        elif "arm64" in filename:
            arch = "arm64"

    return platform, arch

def extract_version(tag):
    # Match pattern like 6.14.0 in frostwire-desktop-6.14.0-build-326
    match = re.search(r"\d+\.\d+\.\d+", tag)
    return match.group(0) if match else "Unknown"

def main():
    response = requests.get(GITHUB_API)
    release = response.json()
    version = extract_version(release["tag_name"])
    assets = release.get("assets", [])

    result = []

    for asset in assets:
        file_name = asset["name"]
        download_url = asset["browser_download_url"]

        platform, arch = detect_platform_arch(file_name)

        if platform == "Unknown" or arch == "Unknown":
            continue

        result.append({
            "product": PRODUCT,
            "version": version,
            "file_name": file_name,
            "url": download_url,
            "platform": platform,
            "architecture": arch
        })

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Saved {len(result)} entries to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
