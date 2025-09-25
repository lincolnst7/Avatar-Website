import json

def standardize_bending(data):
    for character in data:
        if isinstance(character['Bending type'], str) and character['Bending type'] != 'None':
            character['Bending type'] = [character['Bending type']]
    return data

def main():
    # Read the JSON file
    with open('database/avatar_characters.json', 'r') as f:
        data = json.load(f)

    # Standardize the bending types
    standardized_data = standardize_bending(data)

    # Write back to file with consistent formatting
    with open('database/avatar_characters.json', 'w') as f:
        json.dump(standardized_data, f, indent=2)

if __name__ == "__main__":
    main()