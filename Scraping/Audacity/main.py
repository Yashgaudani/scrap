import requests
import json
import os
import re

GITHUB_API_URL = "https://api.github.com/repos/audacity/audacity/releases/latest"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/Audacity/audacity_downloads.json"
PRODUCT_NAME = "Audacity"

ARCH_PATTERN = re.compile(r"(x64|x86_64|64bit|32bit|x86|arm64|universal)", re.IGNORECASE)
PLATFORM_MAP = {
    "win": "Windows",
    "mac": "macOS",
    "macos": "macOS",
    "linux": "Linux"
}

def infer_platform_and_arch(file_name):
    platform = "Unknown"
    architecture = "Unknown"
    lower_name = file_name.lower()

    for key, val in PLATFORM_MAP.items():
        if key in lower_name:
            platform = val
            break

    match = ARCH_PATTERN.search(lower_name)
    if match:
        arch_raw = match.group(1).lower()
        if arch_raw in ["x64", "64bit", "x86_64"]:
            architecture = "x64"
        elif arch_raw in ["32bit", "x86"]:
            architecture = "x86"
        elif arch_raw == "arm64":
            architecture = "arm64"
        elif arch_raw == "universal":
            architecture = "universal"

    # Special handling for .tar.gz
    if lower_name.endswith(".tar.gz") and platform == "Unknown":
        platform = "Linux"

    return platform, architecture

def fetch_latest_audacity_assets():
    response = requests.get(GITHUB_API_URL)
    response.raise_for_status()
    data = response.json()

    version_tag = data.get("tag_name", "").replace("Audacity-", "")
    assets = data.get("assets", [])

    result = []

    for asset in assets:
        file_name = asset.get("name")
        download_url = asset.get("browser_download_url")

        if not file_name or not download_url:
            continue

        # Skip irrelevant files
        if any(file_name.endswith(ext) for ext in [".sig", ".sha256", "CHECKSUMS.txt"]):
            continue

        # Skip GitHub auto-generated source archives
        if file_name.lower().startswith("source code"):
            continue

        # Determine platform and architecture
        platform, architecture = infer_platform_and_arch(file_name)

        entry = {
            "product": PRODUCT_NAME,
            "version": version_tag,
            "file_name": file_name,
            "url": download_url,
            "platform": platform,
            "architecture": architecture
        }

        result.append(entry)

    return result

def main():
    try:
        entries = fetch_latest_audacity_assets()
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

        with open(OUTPUT_PATH, "w") as f:
            json.dump(entries, f, indent=2)

        print(f"✅ JSON saved to: {OUTPUT_PATH}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
