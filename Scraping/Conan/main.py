import requests
import json

# GitHub API URL
url = "https://api.github.com/repos/conan-io/conan/releases/latest"

# Output file path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/Conan/conan_latest.json"

# Helper functions
def detect_platform(name):
    name = name.lower()
    if "windows" in name:
        return "Windows"
    elif "macos" in name:
        return "macOS"
    elif "linux" in name or name.endswith(".deb") or name.endswith(".tgz"):
        return "Linux"
    else:
        return "Unknown"

def detect_architecture(name):
    name = name.lower()
    if "x86_64" in name or "amd64" in name:
        return "x64"
    elif "i686" in name or "win32" in name:
        return "x86"
    elif "arm64" in name or "aarch64" in name:
        return "arm64"
    else:
        return "Unknown"

# Fetch release data
response = requests.get(url)
release = response.json()

# Build output
output = []
for asset in release["assets"]:
    name = asset["name"]
    if name.endswith(".asc") or name.endswith("SHA-256.txt"):
        continue  # Skip irrelevant files

    output.append({
        "product": "Conan Package Manager",
        "version": release["tag_name"],
        "file_name": name,
        "url": asset["browser_download_url"],
        "platform": detect_platform(name),
        "architecture": detect_architecture(name)
    })

# Save to JSON file
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"✔ JSON data saved to: {output_path}")
