import requests
import json
import re

# GitLab API URL for latest Graphviz releases
url = "https://gitlab.com/api/v4/projects/graphviz%2Fgraphviz/releases"

# Output path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/Graphviz/graphviz_latest.json"

# Detect platform from filename
def detect_platform(name):
    name = name.lower()
    if "windows" in name or ".win64" in name or ".win32" in name or name.endswith(".exe") or name.endswith(".msi"):
        return "Windows"
    elif "darwin" in name or name.endswith(".dmg"):
        return "macOS"
    elif "fedora" in name or "ubuntu" in name or "rocky" in name or name.endswith(".rpm") or name.endswith(".deb") or name.endswith(".tar.gz") or name.endswith(".tar.xz"):
        return "Linux"
    elif "cygwin" in name:
        return "Cygwin"
    elif "msys2" in name:
        return "MSYS2"
    else:
        return "Unknown"

# Detect architecture from filename
def detect_architecture(name):
    name = name.lower()
    if "win64" in name or "x86_64" in name or "amd64" in name:
        return "x64"
    elif "win32" in name or "x86" in name or "i386" in name:
        return "x86"
    elif "arm64" in name or "aarch64" in name:
        return "arm64"
    else:
        return "Unknown"

# Fetch release metadata
response = requests.get(url)
releases = response.json()

# Process latest release
latest = releases[0]
version = latest.get("tag_name", "Unknown")

output = []

for asset in latest.get("assets", {}).get("links", []):
    name = asset.get("name") or asset.get("url").split("/")[-1]

    # Skip checksum and signature files
    if name.endswith(".sha256") or name.endswith(".sig"):
        continue

    output.append({
        "product": "Graphviz",
        "version": version,
        "file_name": name,
        "url": asset.get("url"),
        "platform": detect_platform(name),
        "architecture": detect_architecture(name)
    })

# Save JSON
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"✔ Metadata for Graphviz {version} saved to: {output_path}")
