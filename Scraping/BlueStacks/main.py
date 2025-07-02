import xml.etree.ElementTree as ET
import os
import json
import re

# Input RSS file path
rss_path = "/home/yash-gaudani/Downloads/rss-6"

# Output JSON file path
output_json_path = "/home/yash-gaudani/R%D/patch/Scraping/BlueStacks/bluestacks_patches.json"

# Load and parse XML
tree = ET.parse(rss_path)
root = tree.getroot()

data = []

# Regex to extract version from file name
version_pattern = re.compile(r'BlueStacks(?:Installer|_X)?[_\-]?(\d+\.\d+\.\d+\.\d+)')

for item in root.findall('./channel/item'):
    link = item.findtext('link').strip()
    file_name = os.path.basename(link.split('/download')[0])

    # Extract file extension
    file_type = file_name.split('.')[-1].lower() if '.' in file_name else 'unknown'

    # Determine platform
    if file_type == 'exe':
        platform = 'Windows'
    elif file_type == 'dmg':
        platform = 'macOS'
    else:
        platform = 'Unknown'

    # Extract version using regex
    match = version_pattern.search(file_name)
    version = match.group(1) if match else ""

    data.append({
        "product": "BlueStacks",
        "version": version,
        "file_name": file_name,
        "file_type": file_type,
        "url": link,
        "platform": platform
    })

# Save to JSON
with open(output_json_path, 'w') as f:
    json.dump(data, f, indent=4)

print(f"✅ JSON saved to: {output_json_path}")
