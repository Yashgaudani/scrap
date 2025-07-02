import xml.etree.ElementTree as ET
import json
import os
import re

# Input RSS file path
rss_file = '/home/yash-gaudani/Downloads/rss'

# Output directory and file path
output_dir = '/home/yash-gaudani/R%D/patch/Scraping/torbrawer'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'tortoisesvn_patch.json')

# Parse RSS
tree = ET.parse(rss_file)
root = tree.getroot()

# Prepare result list
results = []

# Iterate over all <item> elements
for item in root.findall('.//item'):
    title_elem = item.find('title')
    link_elem = item.find('link')
    
    if title_elem is not None and link_elem is not None:
        title = title_elem.text.strip()
        link = link_elem.text.strip()

        # Extract version from title
        version_match = re.search(r'(\d+\.\d+\.\d+)', title)
        version = version_match.group(1) if version_match else ""

        # Determine architecture from filename
        if 'x64' in title.lower():
            architecture = 'x64'
        elif 'arm64' in title.lower():
            architecture = 'ARM64'
        elif 'x86' in title.lower() or 'win32' in title.lower():
            architecture = 'x86'
        else:
            architecture = 'Unknown'

        results.append({
            "product": "TortoiseSVN",
            "version": version,
            "text": title,
            "url": link,
            "platform": "Windows",
            "architecture": architecture
        })

# Save all entries to JSON
with open(output_file, 'w') as f:
    json.dump(results, f, indent=4)

print(f"Saved {len(results)} entries to: {output_file}")
