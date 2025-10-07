import requests
import json
import re
import os

GITHUB_API = "https://api.github.com/repos/wireapp/wire-desktop/releases"
PRODUCT = "Wire Desktop"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/Wire/wire.json"

# Inference from filename
def infer_platform_arch(filename):
    name = filename.lower()
    if name.endswith(".exe"):
        return ("Windows", "x64")
    elif name.endswith(".dmg") or name.endswith(".pkg"):
        return ("macOS", "Universal")
    elif name.endswith(".AppImage") or name.endswith(".tar.gz") or name.endswith(".deb") or name.endswith(".rpm"):
        return ("Linux", "x64")
    return (None, None)

# Extract version from filename or tag
def extract_version(text):
    match = re.search(r"\b(\d+\.\d+\.\d+)\b", text)
    return match.group(1) if match else None

def main():
    response = requests.get(GITHUB_API)
    response.raise_for_status()
    releases = response.json()

    latest = {}

    for release in releases:
        tag_ver = extract_version(release.get("tag_name", ""))
        for asset in release.get("assets", []):
            fname = asset["name"]
            url = asset["browser_download_url"]
            version = extract_version(fname) or tag_ver
            platform, arch = infer_platform_arch(fname)

            if not platform or not arch or not version:
                continue

            if platform not in latest or version > latest[platform]["version"]:
                latest[platform] = {
                    "product": PRODUCT,
                    "version": version,
                    "file_name": fname,
                    "url": url,
                    "platform": platform,
                    "architecture": arch
                }

    # Save results
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(list(latest.values()), f, indent=2)

    print(f"✅ Found and saved {len(latest)} platforms to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
