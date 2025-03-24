import os
import json

# Directories
root_dir = r"path_to_main_directory"  # Replace with the root directory path
output_dir = r"path_to_output_directory"  # Replace with your desired output directory

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Traverse directories to find 'Cities' folders
for root, dirs, files in os.walk(root_dir):
    if "Cities" in root:  # Focus only on "Cities" folders
        city_name = os.path.basename(os.path.dirname(root))  # Get the parent folder name (city name)
        merged_data = {"city": city_name, "buildingCodes": []}  # Prepare structure for merged data

        # Process each JSON file in the "Cities" folder
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as json_file:
                    try:
                        data = json.load(json_file)  # Load JSON content
                        # Add the building code data to the list
                        merged_data["buildingCodes"].append(data)
                    except json.JSONDecodeError:
                        print(f"Error reading JSON file: {file_path}")

        # Save the merged data for the city
        output_file = os.path.join(output_dir, f"{city_name}_merged.json")
        with open(output_file, "w") as output_json:
            json.dump(merged_data, output_json, indent=4)
        print(f"Merged data saved for {city_name} in {output_file}")

print("Processing complete!")
