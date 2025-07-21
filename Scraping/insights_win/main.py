import requests
import json
import re
import os

GITHUB_API_URL = "https://api.github.com/repos/microsoft/accessibility-insights-windows/releases/latest"
PRODUCT_NAME = "Accessibility Insights for Windows"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/insights_win/accessibility_insights_windows.json"

def infer_platform_and_arch(file_name):
    platform = "Windows"
    architecture = "x64" if "x64" in file_name.lower() or file_name.lower().endswith(".msi") else "Unknown"
    return platform, architecture

def fetch_latest_release():
    response = requests.get(GITHUB_API_URL)
    response.raise_for_status()
    data = response.json()

    version = data["tag_name"].lstrip("v")
    results = []

    for asset in data.get("assets", []):
        file_name = asset["name"]
        url = asset["browser_download_url"]
        platform, architecture = infer_platform_and_arch(file_name)

        results.append({
            "product": PRODUCT_NAME,
            "version": version,
            "file_name": file_name,
            "url": url,
            "platform": platform,
            "architecture": architecture
        })

    return results

def save_to_json(data, file_path=OUTPUT_PATH):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ JSON saved to {file_path}")

if __name__ == "__main__":
    try:
        release_data = fetch_latest_release()
        save_to_json(release_data)
    except Exception as e:
        print(f"❌ Error: {e}")
