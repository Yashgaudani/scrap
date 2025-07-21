import xml.etree.ElementTree as ET
import json
import os

# Local RSS file path
rss_path = "/home/yash-gaudani/Downloads/rss"

# Output JSON file path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/openoffice/openoffice_latest.json"

# Parse RSS XML
tree = ET.parse(rss_path)
root = tree.getroot()

# Output structure
output = []

# Iterate over <item> elements
for item in root.findall(".//item"):
    title = item.findtext("title")
    link = item.findtext("link")
    pub_date = item.findtext("pubDate")
    enclosure = item.find("enclosure")
    file_name = title if title else os.path.basename(link)
    
    # Skip if no valid URL or file extension
    if not link or not file_name.endswith((".exe", ".msi", ".dmg", ".deb", ".rpm", ".tar.gz", ".tar.xz")):
        continue

    # Detect platform
    name = file_name.lower()
    if "win" in name or name.endswith((".exe", ".msi")):
        platform = "Windows"
    elif "mac" in name or name.endswith(".dmg"):
        platform = "macOS"
    elif name.endswith((".deb", ".rpm", ".tar.gz", ".tar.xz")):
        platform = "Linux"
    else:
        platform = "Unknown"

    # Detect architecture
    if "x64" in name or "x86_64" in name or "amd64" in name:
        architecture = "x64"
    elif "x86" in name or "win32" in name or "i386" in name:
        architecture = "x86"
    elif "arm64" in name or "aarch64" in name:
        architecture = "arm64"
    else:
        architecture = "Unknown"

    # Detect version from filename using pattern
    version = "Unknown"
    import re
    version_match = re.search(r"\d+\.\d+(?:\.\d+)?", file_name)
    if version_match:
        version = version_match.group(0)

    output.append({
        "product": "OpenOffice",
        "version": version,
        "file_name": file_name,
        "url": link,
        "platform": platform,
        "architecture": architecture
    })

# Save JSON
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"✔ Structured metadata saved to: {output_path}")
