import requests
import json
import os
from packaging import version as pkg_version

# Output path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/obs_studio/obs_studio_downloads.json"

# GitHub Releases API
api_url = "https://api.github.com/repos/obsproject/obs-studio/releases"

# Detect platform from asset name
def detect_platform(name):
    name = name.lower()
    if 'win' in name and '64' in name:
        return "Windows 64-bit"
    elif 'win' in name and '32' in name:
        return "Windows 32-bit"
    elif 'mac' in name or name.endswith('.dmg'):
        return "macOS"
    elif 'linux' in name or name.endswith(('.appimage', '.tar.gz', '.deb', '.rpm')):
        return "Linux"
    return "Unknown"

# Exclude pre-release tags
def is_stable(tag):
    tag = tag.lower()
    return "rc" not in tag and "beta" not in tag

# Fetch all releases
response = requests.get(api_url)
releases = response.json()

# Filter stable releases and find the latest one
stable_releases = [r for r in releases if is_stable(r.get("tag_name", ""))]
latest_release = max(stable_releases, key=lambda r: pkg_version.parse(r["tag_name"]))

# Parse latest release assets
version = latest_release["tag_name"]
result = []

for asset in latest_release.get("assets", []):
    name = asset.get("name", "")
    url = asset.get("browser_download_url", "")
    platform = detect_platform(name)
    result.append({
        "product": "obs-studio",
        "version": version,
        "text": name,
        "url": url,
        "platform": platform
    })

# Ensure output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save to JSON
with open(output_path, "w") as f:
    json.dump(result, f, indent=4)

print(f"✅ Latest OBS Studio version ({version}) saved to: {output_path}")
