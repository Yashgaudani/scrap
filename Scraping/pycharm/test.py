import requests
import os
import json

# API URL
url = "https://data.services.jetbrains.com/products/releases?code=PCP&type=release&latest=true&platform=linux"
response = requests.get(url)
data = response.json()

# Extract required fields
entry = data["PCP"][0]
version = entry["version"]
downloads = entry["downloads"]

# Platform mapping
platform_map = {
    "windows": "Windows",
    "windowsZip": "Windows",
    "windowsARM64": "Windows",
    "windowsZipARM64": "Windows",
    "mac": "macOS",
    "macM1": "macOS",
    "linux": "Linux",
    "linuxARM64": "Linux"
}

# Prepare output
result = []
for key, value in downloads.items():
    if key in platform_map:
        result.append({
            "product": "PyCharm Professional",
            "file_name": os.path.basename(value["link"]),
            "version": version,
            "download_url": value["link"],
            "platform": platform_map[key]
        })

# Target file path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/pycharm/pycharm_downloads.json"

# Ensure directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save to file
with open(output_path, "w") as f:
    json.dump(result, f, indent=4)

print(f"✅ JSON data saved to: {output_path}")
