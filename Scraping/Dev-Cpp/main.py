import xml.etree.ElementTree as ET
import json
import os
import re

# Local RSS file path
rss_path = "/home/yash-gaudani/Downloads/rss-1"

# Output JSON file path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/Dev-Cpp/devcpp_latest.json"

# Load and parse RSS
tree = ET.parse(rss_path)
root = tree.getroot()

# Output structure
output = []

# Process each <item>
for item in root.findall(".//item"):
    title = item.findtext("title")
    link = item.findtext("link")
    file_name = title or os.path.basename(link)

    # Filter supported file extensions
    if not link or not file_name.endswith((".exe", ".zip", ".msi")):
        continue

    # Detect platform
    name = file_name.lower()
    if name.endswith((".exe", ".msi", ".zip")):
        platform = "Windows"
    else:
        platform = "Unknown"

    # Detect architecture
    if "x64" in name or "x86_64" in name or "amd64" in name:
        architecture = "x64"
    elif "x86" in name or "i386" in name or "32" in name:
        architecture = "x86"
    else:
        architecture = "Unknown"

    # Detect version using regex
    version_match = re.search(r"\d+\.\d+(?:\.\d+)?", file_name)
    version = version_match.group(0) if version_match else "Unknown"

    # Append record
    output.append({
        "product": "Dev-C++",
        "version": version,
        "file_name": file_name,
        "url": link,
        "platform": platform,
        "architecture": architecture
    })

# Save JSON output
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"✔ Metadata for Dev-C++ saved to: {output_path}")
