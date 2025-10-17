#!/usr/bin/env python3
"""
Script to add a "Hints" column with empty arrays to avatar_characters.json
"""

import json
import os
from datetime import datetime

def add_hints_column():
    """Add a "Hints" column with empty arrays to each character entry"""
    
    # Define file paths
    json_file_path = "database/avatar_characters.json"
    backup_file_path = f"database/avatar_characters_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Check if the file exists
    if not os.path.exists(json_file_path):
        print(f"Error: {json_file_path} not found!")
        return False
    
    try:
        # Read the current JSON file
        print(f"Reading {json_file_path}...")
        with open(json_file_path, 'r', encoding='utf-8') as file:
            characters = json.load(file)
        
        # Create a backup of the original file
        print(f"Creating backup: {backup_file_path}")
        with open(backup_file_path, 'w', encoding='utf-8') as backup_file:
            json.dump(characters, backup_file, indent=2, ensure_ascii=False)
        
        # Add "Hints" column to each character
        print("Adding 'Hints' column to each character...")
        updated_count = 0
        
        for character in characters:
            # Check if "Hints" column already exists
            if "Hints" not in character:
                character["Hints"] = []
                updated_count += 1
            else:
                print(f"Warning: 'Hints' column already exists for {character.get('Name', 'Unknown')}")
        
        # Write the updated data back to the file
        print(f"Writing updated data to {json_file_path}...")
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(characters, file, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully added 'Hints' column to {updated_count} characters")
        print(f"📁 Backup saved as: {backup_file_path}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format - {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Starting script to add 'Hints' column...")
    print("=" * 50)
    
    success = add_hints_column()
    
    print("=" * 50)
    if success:
        print("✅ Script completed successfully!")
    else:
        print("❌ Script failed!")

if __name__ == "__main__":
    main()