import requests
import json
import os

GITHUB_API_URL = "https://api.github.com/repos/stefankueng/BowPad/releases/latest"
OUTPUT_DIR = "/home/yash-gaudani/R%D/patch/Scraping/BowPad"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "BowPad.json")

PRODUCT_NAME = "BowPad"

# Map architecture from filename
def detect_architecture(filename):
    if "ARM64" in filename:
        return "ARM64"
    elif "64" in filename:
        return "x64"
    elif "portable" in filename or filename.endswith(".msi") or "BowPad-" in filename:
        return "x86"
    return "unknown"

# Fetch latest release
response = requests.get(GITHUB_API_URL)
release = response.json()
version = release["tag_name"]
assets = release["assets"]

results = []

for asset in assets:
    name = asset["name"]
    url = asset["browser_download_url"]

    if not name.lower().endswith((".msi", ".zip")):
        continue

    architecture = detect_architecture(name)

    results.append({
        "product": PRODUCT_NAME,
        "version": version,
        "file_name": name,
        "url": url,
        "platform": "Windows",
        "architecture": architecture
    })

# Ensure directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Save to JSON file
with open(OUTPUT_FILE, "w") as f:
    json.dump(results, f, indent=2)

print(f"Saved {len(results)} records to {OUTPUT_FILE}")
