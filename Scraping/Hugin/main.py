import xml.etree.ElementTree as ET
import json
import re
import os

# Path to your local XML file
XML_PATH = "file:///home/yash-gaudani/Downloads/rss"
XML_FILE = XML_PATH.replace("file://", "")
OUTPUT_FILE = "/home/yash-gaudani/R%D/patch/Scraping/Hugin/hugin.json"

def extract_version(filename):
    # Capture version like 2024.0.1b and trim suffix if it's a beta indicator
    match = re.search(r"(\d+\.\d+(?:\.\d+)?)([a-z]*)", filename, re.IGNORECASE)
    if match:
        version = match.group(1)
        suffix = match.group(2).lower()
        # Remove suffix if it's a known unstable tag
        if suffix in {"b", "beta", "rc", "alpha"}:
            return version
        return version + suffix
    return ""

def is_stable_release(filename):
    # Lowercase filename for matching
    name = os.path.splitext(filename)[0].lower()
    # Exclude beta, rc, alpha, and trailing "b" (like 1b)
    return not re.search(r"(?:[^a-z]|^)(beta|b\d*|rc\d*|alpha)(?:[^a-z]|$)", name)

def parse_hugin_rss(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    channel = root.find("channel")
    items = channel.findall("item")

    result = []

    for item in items:
        title = item.findtext("title", "").strip()
        download_url = item.findtext("link", "").strip()
        file_name = os.path.basename(title)

        if not is_stable_release(file_name):
            continue

        version = extract_version(file_name)

        result.append({
            "product": "Hugin",
            "version": version,
            "file_name": file_name,
            "download_url": download_url
        })

    return result

if __name__ == "__main__":
    try:
        data = parse_hugin_rss(XML_FILE)
        with open(OUTPUT_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Successfully saved {len(data)} records to '{OUTPUT_FILE}'")
    except Exception as e:
        print(f"❌ Error: {e}")
