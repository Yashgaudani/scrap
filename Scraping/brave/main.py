import requests
import json
import os
import re

# Step 1: Get the latest release metadata from GitHub API
latest_url = "https://api.github.com/repos/brave/brave-browser/releases/latest"
headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Mozilla/5.0"
}

# Request latest release
latest_resp = requests.get(latest_url, headers=headers)
latest_resp.raise_for_status()
latest_data = latest_resp.json()
latest_version = latest_data.get("tag_name", "")
print(f"[✓] Latest version detected: {latest_version}")

# Step 2: Parse assets directly from latest release
results = []
assets = latest_data.get("assets", [])

for asset in assets:
    name = asset.get("name", "")
    download_url = asset.get("browser_download_url", "")

    # OS detection
    if ".exe" in name or ".zip" in name:
        os_name = "Windows"
    elif ".dmg" in name:
        os_name = "macOS"
    elif ".deb" in name or ".tar.gz" in name or ".rpm" in name:
        os_name = "Linux"
    else:
        os_name = "Other"

    # Architecture
    arch_match = re.search(r"(aarch64|arm64|x86_64|amd64|x86)", name)
    architecture = arch_match.group(1) if arch_match else "unknown"

    # Edition
    edition = "Community" if "ce" in name.lower() else "Professional"

    # Download Type
    ext = os.path.splitext(name)[1]
    download_type = ext.replace(".", "").upper() if ext else "UNKNOWN"

    results.append({
        "version": latest_version,
        "os_name": os_name,
        "architecture": architecture,
        "edition": edition,
        "download_type": download_type,
        "download_link": download_url
    })

# Step 3: Save the results
output_path = "brave_downloads.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)

print(f"[✓] Saved {len(results)} entries to: {os.path.abspath(output_path)}")
