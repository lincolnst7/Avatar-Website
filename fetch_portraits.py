import json
import requests
from bs4 import BeautifulSoup
import time

# Path to your characters JSON
INPUT_FILE = "database/avatar_characters.json"
OUTPUT_FILE = "database/avatar_characters_updated.json"

BASE_URL = "https://avatar.fandom.com/wiki/"

# Load JSON
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for char in data:
    if char.get("Image") == "IMAGE_URL_HERE":
        name = char["Name"].replace(" ", "_")
        url = f"{BASE_URL}{name}"
        print(f"Fetching {url}...")

        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")

            # Grab the main infobox portrait
            img_tag = soup.select_one(".pi-image-thumbnail")
            if img_tag and img_tag.get("src"):
                char["Image"] = img_tag["src"]
                print(f" → Found: {char['Image']}")
            else:
                print(" → No portrait found, leaving placeholder")

        except Exception as e:
            print(f"Error fetching {url}: {e}")

        # Be polite to Fandom servers
        time.sleep(1)

# Save updated JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Done! Updated file saved as {OUTPUT_FILE}")
