import os
import json
import xml.etree.ElementTree as ET
import re

# Path to your downloaded RSS file
RSS_FILE = "/home/yash-gaudani/Downloads/CrystalDiskInfo.xml"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/crystaldiskinfo/crystaldiskinfo.json"

def extract_version_from_link(link):
    match = re.search(r'/files/([\d.]+)/', link)
    return match.group(1) if match else None

def determine_architecture(file_name):
    if "x64" in file_name or "64" in file_name or "Shizuku" in file_name or "Aoi" in file_name:
        return "x86_64"
    elif "x86" in file_name or "32" in file_name:
        return "x86"
    else:
        return "x86_64"  # default/fallback

def parse_rss_and_generate_json(rss_path):
    tree = ET.parse(rss_path)
    root = tree.getroot()
    channel = root.find("channel")
    items = channel.findall("item")

    results = []

    for item in items:
        title = item.findtext("title")
        link = item.findtext("link")

        if not link.endswith("/download"):
            continue

        file_name = os.path.basename(link.replace("/download", ""))
        version = extract_version_from_link(link)

        if version:
            results.append({
                "product": "CrystalDiskMark",
                "version": version,
                "file_name": file_name,
                "url": link,
                "platform": "Windows",
                "architecture": determine_architecture(file_name)
            })

    return results

def save_json(data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ JSON saved to: {output_path}")

if __name__ == "__main__":
    data = parse_rss_and_generate_json(RSS_FILE)
    save_json(data, OUTPUT_PATH)
