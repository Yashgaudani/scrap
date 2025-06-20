import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# Step 1: GitHub latest release URL
base_url = "https://github.com/obsproject/obs-studio/releases/latest"

# Step 2: Follow redirect to get actual release URL
latest_response = requests.get(base_url, allow_redirects=True)
actual_release_url = latest_response.url
version = actual_release_url.split("/")[-1]  # Get version like '31.0.3'

# Step 3: Get HTML content of that page
release_page = requests.get(actual_release_url).text
soup = BeautifulSoup(release_page, "html.parser")

# Step 4: Find the correct include-fragment for expanded assets
fragment_tag = soup.find("include-fragment", {"src": lambda x: x and "expanded_assets" in x})
if not fragment_tag:
    print("[-] Could not find include-fragment with expanded_assets.")
    exit()

fragment_src = fragment_tag["src"]
full_fragment_url = urljoin("https://github.com", fragment_src)

# Step 5: Fetch expanded assets HTML
assets_response = requests.get(full_fragment_url)
assets_soup = BeautifulSoup(assets_response.text, "html.parser")

# Step 6: Extract download links and format output
links = assets_soup.find_all("a", href=True)
download_data = []

def guess_platform(text):
    text_lower = text.lower()
    if 'windows' in text_lower:
        return "Windows"
    elif 'macos' in text_lower:
        return "macOS"
    elif 'ubuntu' in text_lower:
        return "Ubuntu"
    elif 'linux' in text_lower:
        return "Linux"
    elif 'debian' in text_lower:
        return "Debian"
    elif 'flatpak' in text_lower:
        return "Flatpak"
    elif 'arch' in text_lower:
        return "Arch Linux"
    else:
        return "Other"

for link in links:
    href = link['href']
    if "/download/" in href:
        full_url = urljoin("https://github.com", href)
        text = link.get_text(strip=True)
        platform = guess_platform(text)
        download_data.append({
            "product": "OBS Studio",
            "version": version,
            "text": text,
            "url": full_url,
            "platform": platform
        })



# Optional: Save to file
with open("obs_downloads.json", "w", encoding="utf-8") as f:
    json.dump(download_data, f, indent=4)
