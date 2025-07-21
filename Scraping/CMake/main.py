import requests
import json

# GitHub API for CMake latest release
url = "https://api.github.com/repos/Kitware/CMake/releases/latest"

# Output path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/CMake/cmake_latest.json"

# Detect platform
def detect_platform(name):
    name = name.lower()
    if "windows" in name:
        return "Windows"
    elif "macos" in name:
        return "macOS"
    elif "linux" in name:
        return "Linux"
    elif "sunos" in name:
        return "SunOS"
    else:
        return "Unknown"

# Detect architecture
def detect_architecture(name):
    name = name.lower()
    if "x86_64" in name or "amd64" in name:
        return "x64"
    elif "i386" in name or "x86" in name:
        return "x86"
    elif "arm64" in name or "aarch64" in name:
        return "arm64"
    elif "sparc64" in name:
        return "sparc64"
    elif "universal" in name :
        return "universal"
    else:
        return "Unknown"

# Fetch GitHub release
response = requests.get(url)
release = response.json()

output = []
for asset in release.get("assets", []):
    name = asset["name"]

    # Skip non-installation files
    if name.endswith((".asc", ".sha256", ".txt", ".json", ".sig")) or name.startswith("Source code"):
        continue

    output.append({
        "product": "CMake",
        "version": release["tag_name"],
        "file_name": name,
        "url": asset["browser_download_url"],
        "platform": detect_platform(name),
        "architecture": detect_architecture(name)
    })

# Save JSON
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"✔ JSON saved to: {output_path}")
