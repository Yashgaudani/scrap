import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import json
import re

BASE_URL = "https://builds.balsamiq.com/"

# Step 1: Fetch XML
response = requests.get(BASE_URL)
if response.status_code != 200:
    raise Exception(f"❌ Failed to fetch XML. Status code: {response.status_code}")

# Step 2: Parse XML
root = ET.fromstring(response.text)

# Step 3: Handle namespace
namespace = ''
if root.tag.startswith('{'):
    namespace = root.tag.split('}')[0].strip('{')
    ns = {'ns': namespace}
else:
    ns = {}

contents_path = './/ns:Contents' if ns else './/Contents'
key_tag = 'ns:Key' if ns else 'Key'
date_tag = 'ns:LastModified' if ns else 'LastModified'

# Step 4: Collect all files with date
all_files = []
for content in root.findall(contents_path, ns):
    key_elem = content.find(key_tag, ns)
    date_elem = content.find(date_tag, ns)
    if key_elem is None or date_elem is None:
        continue
    key = key_elem.text.strip()
    if key.endswith("/"):
        continue
    try:
        date = datetime.strptime(date_elem.text.strip(), "%Y-%m-%dT%H:%M:%S.000Z").date()
        all_files.append((key, date))
    except:
        continue

# Step 5: Filter by latest date
if not all_files:
    print("⚠️ No valid files found.")
    exit()

latest_date = max(date for _, date in all_files)

# Step 6: Build JSON results
results = []

for key, date in all_files:
    if date != latest_date:
        continue
    full_url = BASE_URL + key
    filename = key.split("/")[-1]
    
    # Extract version
    version_match = re.search(r'(\d+\.\d+\.\d+)', filename)
    version = version_match.group(1) if version_match else "unknown"

    # Determine platform and label
    if "x64" in filename or "64" in filename:
        platform = "Windows"
        text = "Download for Windows x64"
    elif "x86" in filename or "32" in filename:
        platform = "Windows"
        text = "Download for Windows x86"
    elif filename.endswith(".dmg"):
        platform = "macOS"
        text = "Download for Mac – Intel or Apple Silicon"
    elif filename.endswith(".zip"):
        platform = "Cross-platform"
        text = "Download ZIP Archive"
    else:
        platform = "Unknown"
        text = "Download File"

    # Add installer type
    if filename.endswith(".exe"):
        text += " (Setup EXE)"
    elif filename.endswith(".msi"):
        text += " (MSI Installer)"
    elif filename.endswith(".dmg"):
        text += " (macOS DMG)"

    results.append({
        "product": "balsamiq-wireframes",
        "version": version,
        "text": text,
        "url": full_url,
        "platform": platform
    })

# Step 7: Save JSON to file
output_path = "/home/yash-gaudani/R%D/patch/Scraping/Balsamiq/latest_balsamiq_links.json"
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ JSON saved to {output_path}")
