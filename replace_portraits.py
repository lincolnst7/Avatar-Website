import json
import os
import re
from urllib.parse import urlparse

# Input JSON file (with Fandom image URLs)
INPUT_FILE = "database/avatar_characters_updated.json"

# Output JSON file (with local image paths)
OUTPUT_FILE = "database/avatar_characters_local.json"

# Relative folder from JSON to images
RELATIVE_DIR = "../images/characters"

# Absolute path to images (for checking existence)
IMAGE_DIR = os.path.join("images", "characters")

# Load JSON
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for char in data:
    name = char.get("Name")
    img_url = char.get("Image")

    if not img_url or img_url == "IMAGE_URL_HERE":
        # No image, leave blank
        char["Image"] = ""
        continue

    # Sanitize character name to match downloaded filenames
    safe_name = re.sub(r"[^a-zA-Z0-9]", "_", name)

    # Preserve original extension from old URL
    parsed = urlparse(img_url)
    _, ext = os.path.splitext(parsed.path)
    if not ext:
        ext = ".jpg"  # fallback

    filename = f"{safe_name}{ext}"
    abs_path = os.path.join(IMAGE_DIR, filename)
    rel_path = os.path.join(RELATIVE_DIR, filename).replace("\\", "/")

    # If file exists locally, update JSON with relative path
    if os.path.exists(abs_path):
        char["Image"] = rel_path
    else:
        # File missing, leave blank
        char["Image"] = ""

# Save updated JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Done! Localized JSON saved as {OUTPUT_FILE}")
