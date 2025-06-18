import requests
import json

# --- Configuration ---
GITHUB_TOKEN = "your_token_here"
url = "https://api.github.com/repos/telerik/fiddler-everywhere-docs/contents/release-notes/release-notes.json"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github.v3.raw"
}

# --- Fetch latest version ---
try:
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()
        latest_version = data[0]["version"]

        formatted_data = {
            "product": "fiddler",
            "version": latest_version,
            "text": "Fiddler Everywhere",
            "platforms": {
                "windows": f"https://downloads.getfiddler.com/win/Fiddler%20Everywhere%20{latest_version}.exe",
                "mac_intel": f"https://downloads.getfiddler.com/mac/Fiddler%20Everywhere%20{latest_version}.dmg",
                "mac_arm64": f"https://downloads.getfiddler.com/mac-arm64/Fiddler%20Everywhere%20{latest_version}.dmg",
                "linux": f"https://downloads.getfiddler.com/linux/fiddler-everywhere-{latest_version}.AppImage"
            }
        }

        with open("fiddler_all_platforms.json", "w") as f:
            json.dump(formatted_data, f, indent=2)
        print("✅ All platform URLs saved to fiddler_all_platforms.json")
    else:
        print(f"❌ Failed to fetch data: {response.status_code}")

except Exception as e:
    print("❌ Error:", e)
