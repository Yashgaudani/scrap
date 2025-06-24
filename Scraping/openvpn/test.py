import requests
from bs4 import BeautifulSoup
import json

# URL to scrape
url = "https://openvpn.net/client/"

# Send GET request
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Get all <a> tags with valid hrefs
links = soup.find_all("a", href=True)
link_data = []

for link in links:
    text = link.get_text(strip=True)
    href = link['href']
    full_url = requests.compat.urljoin(url, href)
    if text and href:
        link_data.append({
            "text": text,
            "url": full_url
        })

# Save HTML page
with open("openvpn_client_page.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

# Save links as JSON
with open("openvpn_links.json", "w", encoding="utf-8") as f:
    json.dump(link_data, f, indent=4)

print("✅ Files saved: openvpn_client_page.html, openvpn_links.json")
