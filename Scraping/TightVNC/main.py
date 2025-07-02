import requests
from bs4 import BeautifulSoup
import json
import os
import re

# Target URL
url = 'https://www.tightvnc.com/download.php'

# Fetch page content
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

# Output directory
output_dir = '/home/yash-gaudani/R%D/patch/Scraping/TightVNC'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'tightvnc_patch.json')

# Result container
results = []

# Search for download links
for a_tag in soup.find_all('a', href=True):
    href = a_tag['href']
    text = a_tag.get_text(strip=True)

    # Match typical installer pattern (EXE or MSI)
    if re.search(r'tightvnc-.*\.(exe|msi)', href, re.IGNORECASE):
        filename = os.path.basename(href)
        version_match = re.search(r'(\d+\.\d+\.\d+)', filename)
        version = version_match.group(1) if version_match else ""

        # Detect architecture
        if '64' in filename:
            arch = 'x64'
        elif '32' in filename or 'x86' in filename:
            arch = 'x86'
        else:
            arch = 'Unknown'

        # Full URL
        full_url = href if href.startswith('http') else f'https://www.tightvnc.com/{href.lstrip("/")}'

        results.append({
            "product": "TightVNC",
            "version": version,
            "text": filename,
            "url": full_url,
            "platform": "Windows",
            "architecture": arch
        })

# Save as JSON
with open(output_file, 'w') as f:
    json.dump(results, f, indent=4)

print(f"Saved {len(results)} entries to: {output_file}")
