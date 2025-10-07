import requests
import json
import os

# GitHub API endpoint
api_url = "https://api.github.com/repos/kovidgoyal/calibre/releases/latest"

# Output path
output_dir = "/home/yash-gaudani/R%D/patch/Scraping/calibre"
output_file = os.path.join(output_dir, "calibre_latest.json")

# Architecture mapping
ARCH_MAP = {
    "x86_64": "x86_64",
    "amd64": "x64",
    "64bit": "x64",
    "arm64": "ARM64",
    "aarch64": "ARM64",
}

def detect_platform_and_arch(filename):
    platform = "Unknown"
    architecture = "Unknown"

    if filename.endswith(".msi") or filename.endswith(".exe"):
        platform = "Windows"
    elif filename.endswith(".dmg"):
        platform = "macOS"
    elif filename.endswith(".txz") or "linux" in filename.lower():
        platform = "Linux"

    for key, value in ARCH_MAP.items():
        if key in filename.lower():
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
        url = asset["browser_download_url"]
        platform, architecture = detect_platform_and_arch(file_name)

        results.append({
            "product": "Calibre",
            "version": version,
            "file_name": file_name,
            "url": url,
            "platform": platform,
            "architecture": architecture
        })

    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write to JSON file
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ JSON saved to: {output_file}")

if __name__ == "__main__":
    main()
