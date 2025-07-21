import requests
import json
import os

GITHUB_API_URL = "https://api.github.com/repos/flameshot-org/flameshot/releases/latest"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/flameshot/flameshot.json"

def extract_info(file_name):
    platform = None
    architecture = None

    if file_name.endswith((".msi", ".zip")):
        platform = "Windows"
        architecture = "x86_64"
    elif file_name.endswith(".dmg"):
        platform = "macOS"
        architecture = "x86_64"
    elif ".arm64" in file_name:
        platform = "Linux"
        architecture = "arm64"
    elif ".armhf" in file_name:
        platform = "Linux"
        architecture = "armhf"
    elif ".amd64" in file_name or ".x86_64" in file_name:
        platform = "Linux"
        architecture = "x86_64"
    elif file_name.endswith((".AppImage", ".flatpak", ".snap")):
        platform = "Linux"
        architecture = "x86_64"

    return platform, architecture

def fetch_flameshot_release_data():
    response = requests.get(GITHUB_API_URL)
    response.raise_for_status()
    release = response.json()
    version = release["tag_name"]
    assets = release["assets"]

    result = []

    for asset in assets:
        name = asset["name"]
        if name.endswith(".sha256sum"):
            continue

        platform, architecture = extract_info(name)
        if platform and architecture:
            result.append({
                "product": "Flameshot",
                "version": version,
                "file_name": name,
                "url": asset["browser_download_url"],
                "platform": platform,
                "architecture": architecture
            })

    return result

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ JSON saved to: {path}")

if __name__ == "__main__":
    data = fetch_flameshot_release_data()
    save_json(data, OUTPUT_PATH)
