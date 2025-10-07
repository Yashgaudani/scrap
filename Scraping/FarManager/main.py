import requests
import re
import json
import os

# Constants
GITHUB_API = "https://api.github.com/repos/FarGroup/FarManager/releases/latest"
PRODUCT = "Far Manager"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/FarManager/farmanager.json"

def parse_filename(filename):
    platform = "Windows"
    arch = "Unknown"

    if ".x86." in filename:
        arch = "x86"
    elif ".x64." in filename:
        arch = "x64"
    elif ".ARM64." in filename:
        arch = "arm64"

    return platform, arch

def extract_version(filename):
    match = re.search(r"\d+\.\d+\.\d+\.\d+", filename)
    return match.group(0) if match else "Unknown"

def main():
    response = requests.get(GITHUB_API)
    response.raise_for_status()
    data = response.json()

    assets = data.get("assets", [])
    results = []

    for asset in assets:
        file_name = asset["name"]
        url = asset["browser_download_url"]

        # Skip non-relevant files like .pdb
        if not file_name.lower().endswith((".msi", ".7z")):
            continue

        version = extract_version(file_name)
        platform, arch = parse_filename(file_name)

        results.append({
            "product": PRODUCT,
            "version": version,
            "file_name": file_name,
            "url": url,
            "platform": platform,
            "architecture": arch
        })

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Save JSON
    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Saved {len(results)} entries to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
