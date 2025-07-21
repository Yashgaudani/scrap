import requests
import os
import json

# GitHub API endpoint for latest release
api_url = "https://api.github.com/repos/adoptium/temurin21-binaries/releases/latest"

# Target directory and file path
output_dir = "/home/yash-gaudani/R%D/patch/Scraping/Eclipse_Jdk"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "temurin21_latest.json")

# Helper function to extract platform
def detect_platform(name):
    name = name.lower()
    if "windows" in name:
        return "Windows"
    elif "linux" in name:
        return "Linux"
    elif "mac" in name or "osx" in name:
        return "macOS"
    elif "aix" in name:
        return "AIX"
    elif "solaris" in name:
        return "Solaris"
    else:
        return "Unknown"

# Helper function to detect type
def detect_type(name):
    name = name.lower()
    if "jdk" in name:
        return "JDK"
    elif "jre" in name:
        return "JRE"
    else:
        return "Unknown"

# Helper function to detect architecture
def detect_architecture(name):
    name = name.lower()
    if "x64" in name or "x86_64" in name:
        return "x64"
    elif "aarch64" in name or "arm64" in name:
        return "aarch64"
    elif "x86" in name:
        return "x86"
    elif "ppc64le" in name:
        return "ppc64le"
    elif "s390x" in name:
        return "s390x"
    elif "sparcv9" in name:
        return "sparcv9"
    elif "riscv64" in name:
        return "riscv64"
    else:
        return "Unknown"

# Fetch data from GitHub API
response = requests.get(api_url)
data = response.json()

version = data["tag_name"].lstrip("jdk-")  # e.g., '21.0.2+13'

output = []

for asset in data.get("assets", []):
    file_name = asset["name"]
    download_url = asset["browser_download_url"]

    # Skip assets that are not JDK or JRE
    type_detected = detect_type(file_name)
    if type_detected not in ["JDK", "JRE"]:
        continue

    platform = detect_platform(file_name)
    arch = detect_architecture(file_name)
    ext = os.path.splitext(file_name)[1]
    if ext == ".gz" and file_name.endswith(".tar.gz"):
        ext = ".tar.gz"
    elif ext == ".pkg" or ext == ".msi" or ext == ".zip":
        ext = ext

    output.append({
        "product": "Eclipse Temurin JRE with Hotspot",
        "version": version,
        "file_name": file_name,
        "url": download_url,
        "platform": platform,
        "architecture": arch,
        "type": type_detected,
        "extension": ext
    })

# Write to JSON file
with open(output_file, "w") as f:
    json.dump(output, f, indent=2)

print(f"✅ Data saved to {output_file}")
