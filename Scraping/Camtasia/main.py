import requests
import json
import os

# Source URL
url = "https://formulae.brew.sh/api/cask/camtasia.json"

# Destination file path
output_dir = "/home/yash-gaudani/R%D/patch/Scraping/Camtasia"
output_file = os.path.join(output_dir, "camtasia_output.json")

# Create directory if not exist
os.makedirs(output_dir, exist_ok=True)

# Fetch JSON data
response = requests.get(url)
response.raise_for_status()
data = response.json()

# Construct output JSON in reference format
output_data = {
    "version": data.get("version", "N/A"),
    "os_name": "macOS",
    "architecture": "x64",
    "download_type": "DMG",
    "download_link": data.get("url", "N/A")
}

# Write to JSON file
with open(output_file, "w") as f:
    json.dump(output_data, f, indent=4)

print(f"Saved to: {output_file}")
