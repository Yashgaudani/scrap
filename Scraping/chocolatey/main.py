import requests
import re
import json
import os

# GitHub API URL
url = "https://api.github.com/repos/chocolatey/ChocolateyGUI/releases/latest"
response = requests.get(url)
response.raise_for_status()
release_data = response.json()

assets = release_data.get("assets", [])
asset_metadata = []

for asset in assets:
    file_name = asset["name"]
    download_url = asset["browser_download_url"]

    # Extract version from download URL
    version_match = re.search(r'/download/([^/]+)/', download_url)
    version = version_match.group(1) if version_match else "unknown"

    # Download type from file extension
    ext = file_name.split('.')[-1].lower()
    if ext == "msi":
        download_type = "msi"
    elif ext == "zip":
        download_type = "zip"
    elif ext == "nupkg":
        download_type = "nupkg"
    elif ext in ["sha256", "txt"]:
        download_type = "checksum"
    else:
        download_type = "other"

    # Architecture and OS
    arch = "x64" if "x64" in file_name.lower() else ("x86" if "x86" in file_name.lower() else "unknown")
    os_name = "windows" if ".msi" in file_name.lower() else "unknown"

    asset_metadata.append({
        "version": version,
        "file_name": file_name,
        "download_type": download_type,
        "architecture": arch,
        "os": os_name,
        "download_link": download_url
    })

# Save to JSON file
output_path = "/home/yash-gaudani/R%D/patch/Scraping/chocolatey/assets_data.json"
with open(output_path, "w") as f:
    json.dump(asset_metadata, f, indent=4)

print(f"✅ JSON saved to: {output_path}")
