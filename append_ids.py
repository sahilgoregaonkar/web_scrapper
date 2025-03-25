import json
import os

def add_new_fields(input_json):
    # Loop through each chapter
    for chapter in input_json.get("chapters", []):
        # Add the new field "projectTypeIds" to each chapter
        chapter["projectTypeIds"] = []
        
        # Loop through each section within the chapter
        for section in chapter.get("sections", []):
            # Add the new field "buildingTypeIds" to each section
            section["buildingTypeIds"] = []

            # Loop through each subsection within the section
            for subsection in section.get("subsections", []):
                # You can add more fields here for subsections if needed.
                subsection["keywords"] = []
                subsection["value"] = []
                subsection["unit"] = []

    return input_json

def update_json_file(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return
    
    # Read the existing JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        input_json = json.load(file)

    # Make changes to the JSON structure
    updated_json = add_new_fields(input_json)

    # Debugging: Show updated JSON before saving
    print("\nUpdated JSON structure:")
    print(json.dumps(updated_json, indent=4))
    
    # Write the updated JSON back to the same file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(updated_json, file, indent=4)
    
    print(f"\nFile '{file_path}' has been updated successfully.")

# Example: Provide the path to your JSON file
file_path = r"C:\Users\Admin\Desktop\web-scrapper\temp_1.json"

# Update the JSON file
update_json_file(file_path)


