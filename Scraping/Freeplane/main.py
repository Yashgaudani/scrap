import os
import xml.etree.ElementTree as ET
import re
import json

# Constants
RSS_PATH = "/home/yash-gaudani/Downloads/rss-2"
OUTPUT_JSON = "/home/yash-gaudani/R%D/patch/Scraping/Freeplane/freeplane.json"
PRODUCT = "Freeplane"
VALID_EXTENSIONS = (".exe", ".deb", ".msi", ".zip", ".dmg")

def extract_version_from_filename(filename):
    match = re.search(r'(\d+\.\d+\.\d+)', filename)
    return match.group(1) if match else None

def detect_platform_and_arch(file_name):
    name = file_name.lower()
    if ".exe" in name or ".msi" in name:
        return "Windows", "x64" if "64" in name or "x64" in name else "x86"
    elif ".deb" in name:
        return "Linux", "x86_64" if "amd64" in name else "x86"
    elif ".dmg" in name:
        return "macOS", "x64"
    else:
        return "Other", "unknown"

def parse_all_latest_versions():
    if not os.path.exists(RSS_PATH):
        print("RSS file not found.")
        return []

    tree = ET.parse(RSS_PATH)
    root = tree.getroot()

    version_file_map = {}

    for item in root.findall("./channel/item"):
        link = item.findtext("link", "").strip()
        if not link.endswith("/download"):
            continue

        filename = os.path.basename(link.replace("/download", ""))
        if not filename.endswith(VALID_EXTENSIONS):
            continue

        version = extract_version_from_filename(filename)
        if not version:
            continue

        platform, arch = detect_platform_and_arch(filename)

        version_file_map.setdefault(version, []).append({
            "product": PRODUCT,
            "version": version,
            "file_name": filename,
            "url": link,
            "platform": platform,
            "architecture": arch
        })

    if not version_file_map:
        return []

    latest_version = sorted(version_file_map.keys(), key=lambda v: list(map(int, v.split('.'))), reverse=True)[0]
    return version_file_map[latest_version]

if __name__ == "__main__":
    latest_data = parse_all_latest_versions()

    if latest_data:
        os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
        with open(OUTPUT_JSON, "w") as f:
            json.dump(latest_data, f, indent=2)
        print(f"✅ Data saved to: {OUTPUT_JSON}")
    else:
        print("❌ No valid entries found.")
