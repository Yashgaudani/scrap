import requests
import os
import json
import re

# GitHub API URL
api_url = "https://api.github.com/repos/ArtifexSoftware/ghostpdl-downloads/releases/latest"

# Output directory and filename
output_dir = "/home/yash-gaudani/R%D/patch/Scraping/Ghostscript"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "ghostscript_latest.json")

# Helper functions
def detect_platform(filename):
    name = filename.lower()
    if "win" in name:
        return "Windows"
    elif name.endswith(".tar.gz") or name.endswith(".tar.xz"):
        return "Linux"
    else:
        return "Unknown"

def detect_architecture(filename):
    name = filename.lower()
    if "64" in name:
        return "x64"
    elif "32" in name:
        return "x86"
    else:
        return "Unknown"

def extract_version(filename):
    match = re.search(r"(\d{2}\.\d{2}\.\d)", filename)
    if match:
        return match.group(1)
    match = re.search(r"gs(\d{5})", filename)
    if match:
        raw = match.group(1)  # e.g., 10051
        return f"{int(raw[:2])}.{int(raw[2:4])}.{int(raw[4])}"
    return "Unknown"

# Fetch release data
response = requests.get(api_url)
release_data = response.json()

output = []

for asset in release_data.get("assets", []):
    file_name = asset["name"]
    download_url = asset["browser_download_url"]

    # Filter by valid extensions
    if not file_name.endswith((".exe", ".zip", ".tar.gz", ".tar.xz")):
        continue

    platform = detect_platform(file_name)
    arch = detect_architecture(file_name)
    version = extract_version(file_name)

    output.append({
        "product": "GPL Ghostscript",
        "version": version,
        "file_name": file_name,
        "url": download_url,
        "platform": platform,
        "architecture": arch
    })

# Save to file
with open(output_file, "w") as f:
    json.dump(output, f, indent=2)

print(f"✅ Data saved to: {output_file}")
