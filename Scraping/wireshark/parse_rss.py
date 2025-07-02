import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import os
import json

# RSS feed URL
url = "https://www.wireshark.org/update/0/Wireshark/3.4.5/Windows/x86-64/en-US/stable.xml"

# Fetch XML
response = requests.get(url)
response.raise_for_status()
root = ET.fromstring(response.content)

# Parse items
data = []
for item in root.findall(".//item"):
    version = item.findtext("title").replace("Version", "").strip()
    enclosure = item.find("enclosure")
    
    if enclosure is not None:
        download_url = enclosure.attrib.get("url")
        file_name = os.path.basename(urlparse(download_url).path)
        
        entry = {
            "product": "Wireshark",
            "version": version,
            "text": file_name,
            "url": download_url,
            "platform": "Windows"
        }
        data.append(entry)

# Save path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/wireshark/wireshark_versions.json"

# Write to JSON
with open(output_path, "w") as f:
    json.dump(data, f, indent=4)

print(f"Saved {len(data)} items to {output_path}")
