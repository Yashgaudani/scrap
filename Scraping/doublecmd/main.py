import requests
import re
import json
import os

# Constants
GITHUB_API = "https://api.github.com/repos/doublecmd/doublecmd/releases/latest"
PRODUCT = "Double Commander"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/doublecmd/doublecmd.json"

def parse_filename(filename):
    platform = "Unknown"
    arch = "Unknown"

    # Determine platform and architecture from filename patterns
    if ".win64" in filename or "-win64" in filename:
        platform = "Windows"
        arch = "x86_64"
    elif ".win32" in filename or "-win32" in filename:
        platform = "Windows"
        arch = "x86"
    elif ".x86_64.AppImage" in filename or ".x86_64.tar.xz" in filename:
        platform = "Linux"
        arch = "x86_64"
    elif ".i386.tar.xz" in filename or ".i386" in filename:
        platform = "Linux" if ".tar.xz"  in filename else "Windows"
        arch = "x86"
    elif "src.tar.gz" in filename:
        platform = "Source"
        arch = "All"

    elif ".aarch64" in filename:
        if filename.endswith(".dmg"):
            platform = "macOS"
        else:
            platform = "Linux"
        arch = "arm64"
    elif ".cocoa.x86_64.dmg" in filename:
        platform = "macOS"
        arch = "x86_64"
    elif ".qt6" in filename:
        platform = "Linux"
        arch = "arm64" if "aarch64" in filename else "x86_64"
    elif ".qt." in filename:
        platform = "Linux"
        arch = "arm64" if "aarch64" in filename else "x86_64"

    return platform, arch

def extract_version(filename):
    match = re.search(r"doublecmd-([0-9]+\.[0-9]+\.[0-9]+)", filename)
    return match.group(1) if match else "Unknown"

def fetch_assets():
    response = requests.get(GITHUB_API)
    data = response.json()
    assets = data.get("assets", [])

    result = []
    for asset in assets:
        file_name = asset["name"]
        url = asset["browser_download_url"]
        platform, arch = parse_filename(file_name)
        version = extract_version(file_name)

        result.append({
            "product": PRODUCT,
            "version": version,
            "file_name": file_name,
            "url": url,
            "platform": platform,
            "architecture": arch
        })

    return result

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ JSON saved to: {path}")

# Main
if __name__ == "__main__":
    releases = fetch_assets()
    save_json(releases, OUTPUT_PATH)
