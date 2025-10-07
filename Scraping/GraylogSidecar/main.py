import requests
import re
import json
import os

# Constants
GITHUB_API = "https://api.github.com/repos/Graylog2/collector-sidecar/releases/latest"
PRODUCT = "Graylog Sidecar"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/GraylogSidecar/graylogsidecar.json"

def detect_platform_arch(filename):
    platform = "Unknown"
    arch = "Unknown"

    if filename.endswith((".msi", ".nupkg")):
        platform = "Windows"
    elif filename.endswith((".rpm", ".deb", ".tar.gz")):
        platform = "Linux"
    elif filename.endswith(".pkg"):
        platform = "macOS"

    if "amd64" in filename or "x86_64" in filename:
        arch = "amd64"
    elif "aarch64" in filename or "arm64" in filename:
        arch = "arm64"
    elif "armv7" in filename:
        arch = "armv7"
    elif "i386" in filename or "x86" in filename:
        arch = "x86"

    return platform, arch

def extract_version(filename):
    match = re.search(r'(\d+\.\d+\.\d+)', filename)
    return match.group(1) if match else "Unknown"

def main():
    try:
        response = requests.get(GITHUB_API)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return

    release = response.json()
    assets = release.get("assets", [])
    results = []

    for asset in assets:
        filename = asset["name"]
        download_url = asset["browser_download_url"]

        if any(ext in filename for ext in [".rpm", ".deb", ".msi", ".tar.gz", ".nupkg"]):
            platform, arch = detect_platform_arch(filename)
            version = extract_version(filename)

            results.append({
                "product": PRODUCT,
                "version": version,
                "file_name": filename,
                "url": download_url,
                "platform": platform,
                "architecture": arch
            })

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Save to JSON file
    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Saved {len(results)} entries to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
