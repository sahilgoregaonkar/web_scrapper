import json
import os

def add_new_fields(input_json):
    # Loop through each chapter
    for chapter in input_json.get("chapters", []):
        # Add the new field "projectTypeIds" with some values
        chapter["projectTypeIds"] = ["A", "B", "E", "F", "H", "I", "M", "R", "S", "U"]
        
        # Loop through each section within the chapter
        for section in chapter.get("sections", []):
            # Add the new field "buildingTypeIds" with some values
            section["buildingTypeIds"] = [
                "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", 
                "A14", "A15", "A16", "A17", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", 
                "B10", "B11", "B12", "B13", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", 
                "E10", "E11", "E12", "E13", "E14", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", 
                "F9", "F10", "F11", "F12", "F13", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", 
                "H9", "H10", "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I10", "M1", 
                "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "R1", "R2", "R3", "R4", 
                "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15", "S1", 
                "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "U1", "U2", "U3", "U4", 
                "U5", "U6", "U7", "U8", "U9", "U10"
            ]

    return input_json

def custom_dumps(data):
    """ Custom function to format arrays horizontally """
    # This modifies how arrays like "projectTypeIds" and "buildingTypeIds" will appear
    return json.dumps(data, indent=4, separators=(',', ': '))

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
    
    # Use the custom function to output the JSON in the desired format
    print(custom_dumps(updated_json))

    # Write the updated JSON back to the same file
    with open(file_path, 'w', encoding='utf-8') as file:
        # Writing the JSON back to the file with proper formatting
        json.dump(updated_json, file, indent=4, separators=(',', ': '))  # Ensures correct formatting
    
    print(f"\nFile '{file_path}' has been updated successfully.")

# Example: Provide the path to your JSON file
file_path = r"C:\Users\Admin\Desktop\web-scrapper\temp_1.json"

# Update the JSON file
update_json_file(file_path)
