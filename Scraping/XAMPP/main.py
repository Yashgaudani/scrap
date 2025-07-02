import xml.etree.ElementTree as ET
import os
import json

# Path to your local RSS file
rss_path = "/home/yash-gaudani/Downloads/rss-1"

# Output JSON file
output_json = "/home/yash-gaudani/R%D/patch/Scraping/XAMPP/xampp_patches.json"

# Load and parse XML
tree = ET.parse(rss_path)
root = tree.getroot()

# Define namespaces (SourceForge uses custom tags)
namespaces = {
    "media": "http://search.yahoo.com/mrss/",
    "files": "https://sourceforge.net/api/file/"
}

patches = []

for item in root.findall(".//item"):
    title = item.findtext("title").strip().split("/")[-1]
    link = item.findtext("link").strip()
    pub_date = item.findtext("pubDate")
    media = item.find("media:content", namespaces)
    file_type = media.attrib.get("type", "") if media is not None else ""
    file_size = int(media.attrib.get("filesize", 0)) if media is not None else 0
    download_url = media.attrib.get("url", "") if media is not None else link
    file_hash = item.findtext("media:hash", default="", namespaces=namespaces)
    
    version = "unknown"
    architecture = "unknown"
    platform = "unknown"

    if "windows" in title.lower():
        platform = "Windows"
    if "x64" in title.lower():
        architecture = "x64"
    if "8.2.12" in title:
        version = "8.2.12"

    patches.append({
        "product": "xampp",
        "version": version,
        "platform": platform,
        "architecture": architecture,
        "file_name": title,
        "download_url": download_url,
        
    })

# Save to JSON
os.makedirs(os.path.dirname(output_json), exist_ok=True)
with open(output_json, "w") as f:
    json.dump(patches, f, indent=4)

print(f"✅ Extracted {len(patches)} entries to: {output_json}")
