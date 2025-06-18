import requests
from bs4 import BeautifulSoup
import json
import os
import re

url = "https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html"
base_url = "https://www.chiark.greenend.org.uk/~sgtatham/putty/"
output_path = "/home/yash-gaudani/R%D/patch/Scraping/putty/putty_msi_links.json"

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

result = []

# Extract all .msi download links
for a in soup.find_all('a', href=True):
    href = a['href']
    if href.endswith('.msi') and 'installer' in href:
        filename = href.split('/')[-1]
        full_url = base_url + filename

        # Extract version from filename
        version_match = re.search(r'putty.*?([0-9]+\.[0-9]+).*?installer\.msi', filename)
        version = version_match.group(1) if version_match else "unknown"

        # Detect architecture
        if "64bit" in filename:
            arch = "64-bit x86"
        elif "arm64" in filename:
            arch = "64-bit Arm"
        elif re.match(r'putty-\d+\.\d+-installer\.msi', filename) or "putty-0" in filename:
            arch = "32-bit x86"
        else:
            arch = "unknown"

        result.append({
            "product": "putty",
            "version": version,
            "text": filename,
            "url": full_url,
            "platform": "Windows"
        })

# Create output directory
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save JSON
with open(output_path, 'w') as f:
    json.dump(result, f, indent=2)

print(f"✅ Saved {len(result)} MSI links to: {output_path}")
