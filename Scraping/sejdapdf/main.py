import requests

# Base URL
url = "https://www.sejda.com/desktop"

# Send HTTP GET request to fetch the page
response = requests.get(url)

# Check for successful response
if response.status_code == 200:
    # Save the HTML content to a file
    with open("sejda_desktop.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("✅ HTML page saved as 'sejda_desktop.html'")
else:
    print(f"❌ Failed to fetch the page. Status code: {response.status_code}")
