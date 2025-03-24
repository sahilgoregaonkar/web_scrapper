import json
import os
from collections import defaultdict

# Path to the folder containing the JSON files
input_folder = r"C:\Users\Admin\Desktop\OP"  # Replace with your folder path

# Path to the folder where the merged files will be saved
output_folder = r"C:\Users\Admin\Desktop\OP\Merged_Files"  # Replace with your desired output folder path

# Make sure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Dictionary to store cities data grouped by city name (e.g., "Accord")
grouped_cities = defaultdict(list)

# List all JSON files in the folder
try:
    json_files = [f for f in os.listdir(input_folder) if f.endswith('.json')]
    if not json_files:
        print("No JSON files found in the input folder.")
except Exception as e:
    print(f"Error listing files in folder: {e}")

# Log found JSON files
print(f"Found {len(json_files)} JSON files.")

# Loop through each file in the folder and extract the "cities" array
for file_name in json_files:
    file_path = os.path.join(input_folder, file_name)
    
    # Extract the city name (after the number and before the comma)
    city_name = file_name.split('_')[1].split(',')[0]
    
    # Open the JSON file and load the data
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            if "cities" in data:
                grouped_cities[city_name].extend(data["cities"])  # Merge the cities data
                print(f"Found 'cities' in {file_name}. Merged {len(data['cities'])} cities for {city_name}.")
            else:
                print(f"Warning: 'cities' key not found in {file_name}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Create merged JSON files for each city and save in the output folder
for city_name, cities in grouped_cities.items():
    if cities:  # Only create a merged file if there are cities
        merged_data = {"cities": cities}
        
        # Output file path based on the city name in the output folder
        output_file = os.path.join(output_folder, f"{city_name}_merged.json")
        
        # Write the merged cities data to a new file in the output folder
        try:
            with open(output_file, 'w') as outfile:
                json.dump(merged_data, outfile, indent=4)
            print(f"Merged cities data for {city_name} has been saved to {output_file}")
        except Exception as e:
            print(f"Error saving merged file {output_file}: {e}")
    else:
        print(f"No cities to merge for {city_name}. Skipping file.")
