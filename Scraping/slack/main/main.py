import requests
import xml.etree.ElementTree as ET
import re
import json
import os
from datetime import datetime
from typing import Dict, Optional

def extract_version(title: str) -> str:
    patterns = [
        r'(\d+\.\d+(?:\.\d+)?)',
        r'Version\s+(\d+\.\d+(?:\.\d+)?)',
        r'v(\d+\.\d+(?:\.\d+)?)'
    ]
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            return match.group(1)
    return "Unknown"

def fetch_latest_slack_update(platform: str = "macos") -> Optional[Dict]:
    try:
        url = f"https://slack.com/intl/en-in/release-notes/{platform}/rss"
        response = requests.get(url)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        namespaces = {'content': 'http://purl.org/rss/1.0/modules/content/'}

        latest_item = None
        latest_date = None

        for item in root.findall("./channel/item"):
            title = item.findtext("title")
            link = item.findtext("link")
            pub_date = item.findtext("pubDate")
            content_encoded = item.find("content:encoded", namespaces).text
            pub_datetime = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')

            if not latest_date or pub_datetime > latest_date:
                latest_date = pub_datetime
                version = extract_version(title)
                links = re.findall(r"https?://[^\s\"<>]+", content_encoded)

                latest_item = {
                    "product": "Slack",
                    "platform": platform,
                    "version": version,
                    "publication_date": pub_date,
                    "url": link,
                    "content_links": links,
                    "last_checked": datetime.now().isoformat()
                }

        return latest_item

    except Exception as e:
        print(f"❌ Error for {platform}: {str(e)}")
        return None

def save_to_file(data: Dict, platform: str) -> bool:
    try:
        output_dir = "/home/yash-gaudani/R%D/Vlc/slack/main"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"slack_updates_{platform}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved to {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving for {platform}: {str(e)}")
        return False

def main():
    for platform in ["mac", "windows", "linux"]:
        print(f"\n🔍 Fetching latest update for: {platform}")
        latest = fetch_latest_slack_update(platform)
        if latest:
            save_to_file(latest, platform)
        else:
            print(f"⚠️ No update found for {platform}")

if __name__ == "__main__":
    main()
