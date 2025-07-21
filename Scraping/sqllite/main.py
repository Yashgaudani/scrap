import requests
import json

# GitHub API URL
url = "https://api.github.com/repos/sqlitebrowser/sqlitebrowser/releases/latest"

# File output path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/sqllite/sqlitebrowser_latest.json"

# Architecture detection
def detect_architecture(filename):
    filename = filename.lower()
    if "win32" in filename or "x86" in filename:
        return "x86"
    elif "win64" in filename or "x64" in filename or "x86_64" in filename:
        return "x64"
    elif "arm64" in filename:
        return "arm64"
    elif "armhf" in filename:
        return "armhf"
    else:
        return "Unknown"

# Platform detection
def detect_platform(filename):
    filename = filename.lower()
    if filename.endswith(".paf.exe") or filename.endswith(".msi") or filename.endswith(".zip") :
        return "Windows"
    elif filename.endswith(".dmg"):
        return "macOS"
    elif filename.endswith(".appimage") or "linux" in filename:
        return "Linux"
    else:
        return "Unknown"

# Fetch and parse
response = requests.get(url)
release_data = response.json()

output = []
for asset in release_data.get("assets", []):
    file_name = asset["name"]
    download_url = asset["browser_download_url"]

    output.append({
        "product": "DB Browser for SQLite",
        "version": release_data["tag_name"],
        "file_name": file_name,
        "url": download_url,
        "platform": detect_platform(file_name),
        "architecture": detect_architecture(file_name)
    })

# Save to JSON file
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"JSON data saved to: {output_path}")
