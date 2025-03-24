import os
import json

def update_name_field(folder_path):
    for filename in os.listdir(folder_path):
        # Process only .json files
        if filename.endswith('.json'):
            # Extract the city name (everything before the first comma or space)
            city_name = filename.split(',')[0].strip()

            # Full path of the JSON file
            file_path = os.path.join(folder_path, filename)
            
            try:
                # Open and load the JSON file
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # Debug: Print the original structure of the JSON
                print(f"Original data in {filename}: {data}")

                # Check if 'cities' field exists and contains data
                if 'cities' in data and isinstance(data['cities'], list):
                    # Iterate over each city in the list and update its 'name' field
                    for city in data['cities']:
                        if 'name' in city:
                            print(f"Before update: {city['name']}")  # Debug: Print current name
                            city['name'] = city_name
                            print(f"After update: {city['name']}")   # Debug: Print updated name
                        else:
                            print(f"Skipping {filename}: 'name' field not found in city.")
                
                # Save the updated JSON file
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4)
                print(f"Updated 'name' field in: {filename}")
                    
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

# Replace with the path to your folder containing the JSON files
folder_path = r"C:\Users\Admin\Desktop\Name_update"
update_name_field(folder_path)
