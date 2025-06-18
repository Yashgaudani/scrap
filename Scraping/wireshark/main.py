import requests
from bs4 import BeautifulSoup

# Base URL
url = "https://2.na.dl.wireshark.org/"

# Fetch the page
response = requests.get(url)
response.raise_for_status()

# Get raw HTML
html_content = response.text

# Optionally parse for a cleaner view (pretty print)
soup = BeautifulSoup(html_content, "html.parser")
pretty_html = soup.prettify()

# Save to file
with open("wireshark_base_page.html", "w", encoding="utf-8") as f:
    f.write(pretty_html)

print("✅ HTML template saved to 'wireshark_base_page.html'")
