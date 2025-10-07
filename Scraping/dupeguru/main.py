import requests
import re
import json
import os

# Constants
GITHUB_API = "https://api.github.com/repos/arsenetar/dupeguru/releases/latest"
PRODUCT = "DupeGuru"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/dupeguru/dupeguru.json"

def parse_filename(filename):
    platform = "Unknown"
    arch = "Unknown"

    # Normalize lowercase
    fname = filename.lower()

    # Platform detection
    if "win64" in fname or "_win64" in fname:
        platform = "Windows"
        arch = "x86_64"
    elif "win32" in fname or "_win32" in fname:
        platform = "Windows"
        arch = "x86"
    elif fname.endswith(".dmg") or "macos" in fname:
        platform = "macOS"
        arch = "x86_64"  # DupeGuru mac builds are usually universal/x86_64
    elif fname.endswith(".rpm") or ".rpm" in fname:
        platform = "Linux"
        arch = "x86_64"
    elif fname.endswith(".deb") or ".amd64.deb" in fname:
        platform = "Linux"
        arch = "x86_64"
    elif fname.endswith(".tar.xz"):
        platform = "Linux"
        arch = "x86_64"  # Source or binary
    elif "amd64" in fname:
        platform = "Linux"
        arch = "x86_64"
    elif "arm64" in fname or "aarch64" in fname:
        platform = "Linux"
        arch = "arm64"

    return platform, arch

def extract_version(filename):
    match = re.search(r"(\d+\.\d+\.\d+)", filename)
    return match.group(1) if match else "Unknown"

def fetch_assets():
    response = requests.get(GITHUB_API)
    data = response.json()
    assets = data.get("assets", [])

    result = []
    for asset in assets:
        file_name = asset["name"]
        if file_name.endswith(".sig"):
            continue  # Skip signature files

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
