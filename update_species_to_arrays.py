#!/usr/bin/env python3
"""
Script to convert all "Species" entries in the Avatar characters JSON database
from single strings to arrays (brackets).

For example:
"Species": "Human" -> "Species": ["Human"]
"Species": "Spirit" -> "Species": ["Spirit"]
"""

import json
import os

def update_species_to_arrays():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the JSON database file (relative to script location)
    json_file_path = os.path.join(script_dir, "database", "avatar_characters.json")
    
    # Check if file exists
    if not os.path.exists(json_file_path):
        print(f"Error: File '{json_file_path}' not found!")
        print("Make sure the database/avatar_characters.json file exists in the same directory as this script.")
        return False
    
    try:
        # Read the JSON file
        print(f"Reading {json_file_path}...")
        with open(json_file_path, 'r', encoding='utf-8') as file:
            characters = json.load(file)
        
        print(f"Loaded {len(characters)} characters.")
        
        # Keep track of changes
        changes_made = 0
        species_types = set()
        
        # Process each character
        for character in characters:
            if "Species" in character:
                current_species = character["Species"]
                
                # Add to species_types set (handle both strings and arrays)
                if isinstance(current_species, str):
                    species_types.add(current_species)
                elif isinstance(current_species, list):
                    for species in current_species:
                        species_types.add(species)
                
                # Check if Species is already an array
                if isinstance(current_species, str):
                    # Convert string to array
                    character["Species"] = [current_species]
                    changes_made += 1
                elif isinstance(current_species, list):
                    # Already an array, no change needed
                    pass
                else:
                    print(f"Warning: Unexpected Species type for character '{character.get('Name', 'Unknown')}': {type(current_species)}")
        
        print(f"\nSpecies types found: {sorted(species_types)}")
        print(f"Changes made: {changes_made}")
        
        if changes_made > 0:
            # Create backup of original file
            backup_path = json_file_path + ".backup"
            print(f"\nCreating backup at {backup_path}...")
            with open(backup_path, 'w', encoding='utf-8') as backup_file:
                json.dump(characters, backup_file, indent=2, ensure_ascii=False)
            
            # Write updated data back to original file
            print(f"Writing updated data to {json_file_path}...")
            with open(json_file_path, 'w', encoding='utf-8') as file:
                json.dump(characters, file, indent=2, ensure_ascii=False)
            
            print(f"✅ Successfully updated {changes_made} characters!")
            print(f"📁 Backup saved as {backup_path}")
        else:
            print("ℹ️ No changes needed - all Species entries are already in array format.")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {json_file_path}")
        print(f"JSON Error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("Avatar Characters Database - Species Array Converter")
    print("=" * 50)
    
    success = update_species_to_arrays()
    
    if success:
        print("\n✅ Script completed successfully!")
    else:
        print("\n❌ Script failed. Please check the errors above.")

if __name__ == "__main__":
    main()