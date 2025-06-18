import requests
from bs4 import BeautifulSoup
import os
import json
from packaging.version import Version

# Configuration
base_url = "https://download.gimp.org/gimp/v3.0/"
platform_dirs = {
    "Windows": "windows/",
    "macOS": "macos/",
    "Linux": "linux/"
}
output_path = "/home/yash-gaudani/R%D/patch/Scraping/gimp/gimp_latest_all.json"

results = []

# Step 1: Loop through platform folders
for platform, subdir in platform_dirs.items():
    url = base_url + subdir
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    for link in soup.find_all('a'):
        filename = link.get('href')
        if not filename or not filename.lower().endswith(('.exe', '.dmg', '.appimage')):
            continue

        # Extract version from filename
        parts = filename.replace('-', '.').replace('_', '.').split('.')
        version_candidates = [p for p in parts if p.replace('v', '').replace('RC', '').isdigit()]
        if version_candidates:
            version = None
            for i in range(len(parts)):
                try:
                    # Try forming a version number from chunks
                    version = Version(".".join(parts[i:i+3]).strip("-"))
                    break
                except:
                    continue
            if version:
                results.append({
                    "product": "GIMP",
                    "version": str(version),
                    "text": filename,
                    "url": url + filename,
                    "platform": platform
                })

# Step 2: Filter only latest version
if results:
    all_versions = {r["version"] for r in results}
    latest_version = max(all_versions, key=Version)
    print(f"✅ Keeping only latest version: {latest_version}")

    results = [r for r in results if r["version"] == latest_version]
else:
    print("⚠️ No results found.")

# Step 3: Save to JSON
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"✅ Saved GIMP {latest_version} download links to: {output_path}")
