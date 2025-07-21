import requests
import json

# GitLab API URL for latest Cherrytree macOS release (from GitLab project: dehesselle/cherrytree_macos)
url = "https://gitlab.com/api/v4/projects/dehesselle%2Fcherrytree_macos/releases"

# Output file path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/CherryTree/cherrytree_gitlab_latest.json"

# Detect platform from filename
def detect_platform(name):
    name = name.lower()
    if name.endswith((".exe", ".msi", ".7z")) or "win" in name:
        return "Windows"
    elif name.endswith((".dmg", ".app")) or "macos" in name or "darwin" in name:
        return "macOS"
    elif name.endswith((".deb", ".rpm", ".tar.gz", ".tar.xz", ".appimage")) or "linux" in name:
        return "Linux"
    else:
        return "Unknown"

# Detect architecture from filename
def detect_architecture(name):
    name = name.lower()
    if "x64" in name or "x86_64" in name or "amd64" in name:
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

# Process latest release only
latest = releases[0]
version = latest.get("tag_name", "Unknown")

output = []

for asset in latest.get("assets", {}).get("links", []):
    name = asset.get("name") or asset.get("url").split("/")[-1]

    # Skip signature and checksum files
    if name.endswith((".sig", ".sha256", ".asc")):
        continue

    output.append({
        "product": "Cherrytree",
        "version": version,
        "file_name": name,
        "url": asset.get("url"),
        "platform": detect_platform(name),
        "architecture": detect_architecture(name)
    })

# Save to JSON file
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"✔ Metadata for Cherrytree {version} saved to: {output_path}")
