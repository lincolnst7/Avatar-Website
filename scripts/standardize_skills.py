import json
import os

def standardize_skills(data):
    for character in data:
        # Handle Special Skills field
        if 'Special Skills' in character:
            # If it's a string, convert to a single-item list
            if isinstance(character['Special Skills'], str):
                character['Special Skills'] = [character['Special Skills']]
            # If it's None or "None", convert to ["None"]
            elif character['Special Skills'] is None:
                character['Special Skills'] = ["None"]
    return data

def main():
    # Get the path to the database file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(script_dir, '..', 'database', 'avatar_characters.json')
    
    # Read the current database
    with open(database_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Standardize the skills
    standardized_data = standardize_skills(data)
    
    # Write back to the file with proper formatting
    with open(database_path, 'w', encoding='utf-8') as f:
        json.dump(standardized_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
