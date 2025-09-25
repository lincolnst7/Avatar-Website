import json

# The standardized appearance strings
VALID_APPEARANCES = [
    "Avatar: The Last Airbender",
    "The Legend of Korra",
    "Avatar Comics",
    "Korra Comics",
    "Kyoshi Novels",
    "Yangchen Novels",
    "Roku Novels",
    "Avatar Novels"
]

def standardize_appearances(data):
    for character in data:
        # Remove any duplicates and sort according to standard order
        appearances = list(set(character["Appearances"]))
        # Filter to only include valid appearances and sort by standard order
        standardized = [app for app in VALID_APPEARANCES if app in appearances]
        # Update the character's appearances
        character["Appearances"] = standardized

    return data

def main():
    # Read the JSON file
    with open('database/avatar_characters.json', 'r') as f:
        data = json.load(f)

    # Standardize the appearances
    standardized_data = standardize_appearances(data)

    # Write back to file with consistent formatting
    with open('database/avatar_characters.json', 'w') as f:
        json.dump(standardized_data, f, indent=2)

if __name__ == "__main__":
    main()