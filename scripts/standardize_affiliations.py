import json

def standardize_affiliations(data):
    for character in data:
        if isinstance(character['Affiliation/Group'], str):
            if character['Affiliation/Group'] == 'None':
                character['Affiliation/Group'] = []
            else:
                character['Affiliation/Group'] = [character['Affiliation/Group']]
    return data

def main():
    # Read the JSON file
    with open('database/avatar_characters.json', 'r') as f:
        data = json.load(f)

    # Standardize the affiliations
    standardized_data = standardize_affiliations(data)

    # Write back to file with consistent formatting
    with open('database/avatar_characters.json', 'w') as f:
        json.dump(standardized_data, f, indent=2)

if __name__ == "__main__":
    main()