import requests
import json

# GitHub API URL for latest release of Client Center
url = "https://api.github.com/repos/rzander/sccmclictr/releases/latest"

# Output file path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/Client_Center/sccmclictr_latest.json"

# Platform detection
def detect_platform(name):
    name = name.lower()
    if name.endswith((".exe", ".msi")) or "windows" in name:
        return "Windows"
    else:
        return "Unknown"

# Architecture detection
def detect_architecture(name):
    name = name.lower()
    if "x64" in name or "x86_64" in name or "amd64" in name:
        return "x64"
    elif "x86" in name or "win32" in name or "i386" in name:
        return "x86"
    else:
        return "Unknown"

# Fetch the latest release info
response = requests.get(url)
release = response.json()
version = release.get("tag_name", "Unknown")

output = []

for asset in release.get("assets", []):
    name = asset["name"]

    # Process only .exe or .msi files
    if not name.lower().endswith((".exe", ".msi")):
        continue

    output.append({
        "product": "Client Center for Configuration Manager",
        "version": version,
        "file_name": name,
        "url": asset["browser_download_url"],
        "platform": detect_platform(name),
        "architecture": detect_architecture(name)
    })

# Save as JSON
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"✔ Metadata saved to: {output_path}")
