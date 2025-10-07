import requests
import re
import json
import os

GITHUB_API = "https://api.github.com/repos/bardsoftware/ganttproject/releases/latest"
PRODUCT = "GanttProject"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/GanttProject/ganttproject.json"

# Mapping function
def get_platform_arch(filename):
    filename_lower = filename.lower()
    if filename.endswith(".exe") or filename.endswith(".msi"):
        return "Windows", "x64"
    elif "intel.dmg" in filename_lower:
        return "macOS", "x64"
    elif "silicon.dmg" in filename_lower:
        return "macOS", "arm64"
    elif filename.endswith(".deb") or filename.endswith(".tar.bz2") or filename.endswith(".zip"):
        return "Linux", "x64"
    return None, None

def main():
    response = requests.get(GITHUB_API)
    data = response.json()
    
    version = re.search(r"(\d+\.\d+\.\d+)", data["tag_name"])
    if not version:
        print("No valid version found in tag.")
        return
    version = version.group(1)

    result = []
    for asset in data.get("assets", []):
        file_name = asset["name"]
        download_url = asset["browser_download_url"]
        platform, architecture = get_platform_arch(file_name)

        if platform:
            result.append({
                "product": PRODUCT,
                "version": version,
                "file_name": file_name,
                "url": download_url,
                "platform": platform,
                "architecture": architecture
            })

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Metadata saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
