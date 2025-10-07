import requests
import json
import os

# Output path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/conemu/conemu.json"

# GitHub API URL
api_url = "https://api.github.com/repos/Maximus5/ConEmu/releases/latest"

# Architecture mapping
ARCH_MAP = {
    "x64": "x64",
    "x86_64": "x64",
    "x86": "x86",
    "arm64": "ARM64",
    "aarch64": "ARM64",
}

def detect_platform_and_arch(filename):
    name = filename.lower()
    platform = "Unknown"
    architecture = "Unknown"

    if name.endswith((".exe", ".7z")):
        platform = "Windows"

    for key, value in ARCH_MAP.items():
        if key in name:
            architecture = value
            break

    return platform, architecture

def main():
    response = requests.get(api_url)
    data = response.json()
    version = data.get("tag_name", "").lstrip("v")

    results = []

    for asset in data.get("assets", []):
        file_name = asset["name"]

        # Skip irrelevant files
        if any(ext in file_name for ext in [".txt", ".sig", "Source code"]):
            continue

        url = asset["browser_download_url"]
        platform, architecture = detect_platform_and_arch(file_name)

        results.append({
            "product": "ConEmu",
            "version": version,
            "file_name": file_name,
            "url": url,
            "platform": platform,
            "architecture": architecture
        })

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write to JSON file
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Data saved to {output_path}")

if __name__ == "__main__":
    main()
