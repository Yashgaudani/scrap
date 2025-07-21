import requests
import xml.etree.ElementTree as ET
import re
import json
from packaging.version import parse as parse_version
import os

BASE_URL = "https://pan-gp-client.s3.amazonaws.com/"
NS_URI = "http://s3.amazonaws.com/doc/2006-03-01/"
KEY_TAG = f".//{{{NS_URI}}}Key"
VERSION_FOLDER_REGEX = re.compile(r"([\d.]+-\d+)/(.+)$")
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/GlobalProtect/latest_globalprotect.json"

def main():
    try:
        print("📥 Fetching XML listing...")
        resp = requests.get(BASE_URL)
        resp.raise_for_status()
    except Exception as e:
        print("❌ Failed to fetch XML:", e)
        return

    root = ET.fromstring(resp.content)
    keys = [elem.text for elem in root.findall(KEY_TAG)]

    version_map = {}

    for key in keys:
        match = VERSION_FOLDER_REGEX.search(key)
        if not match:
            continue

        version_str, filename = match.groups()
        version_obj = parse_version(version_str.replace("-", "."))

        if version_obj not in version_map:
            version_map[version_obj] = []

        url = BASE_URL + key

        # Determine platform from file extension
        if filename.endswith((".msi", ".exe", ".zip")):
            platform = "Windows"
        elif filename.endswith(".pkg"):
            platform = "macOS"
        elif filename.endswith((".deb", ".rpm", ".tar.gz")):
            platform = "Linux"
        else:
            platform = "Unknown"

        # Determine architecture from filename
        filename_lower = filename.lower()
        if "64" in filename_lower:
            architecture = "64-bit"
        elif "32" in filename_lower:
            architecture = "32-bit"
        else:
            architecture = "Unknown"

        result = {
            "product": "GlobalProtect",
            "version": version_str,
            "file_name": filename,
            "url": url,
            "platform": platform,
            "architecture": architecture
        }

        version_map[version_obj].append(result)

    if not version_map:
        print("❌ No matching entries found.")
        return

    # Get latest version
    latest_version = max(version_map.keys())
    latest_data = version_map[latest_version]

    # Write to JSON file
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(latest_data, f, indent=2)

    print(f"✅ Latest version: {latest_data[0]['version']}")
    print(f"📝 Data saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
