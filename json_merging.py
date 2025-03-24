import json
import os

# List of file paths to your JSON files
json_files = [
    r"C:\Users\Admin\Desktop\OP\Accord, NY.json_1",
    r"C:\Users\Admin\Desktop\OP\Accord, NY.json_2",
    r"C:\Users\Admin\Desktop\OP\Accord, NY.json_3",  # Add more paths as necessary
    # Add more files as needed
]

# Dictionary to store cities data grouped by prefix
grouped_cities = {}

# Loop through each file and extract the "cities" array
for file_path in json_files:
    if os.path.exists(file_path):  # Check if file exists
        # Extract the prefix (before the comma)
        prefix = os.path.basename(file_path).split(',')[0]
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            if "cities" in data:
                if prefix not in grouped_cities:
                    grouped_cities[prefix] = []
                grouped_cities[prefix].extend(data["cities"])  # Merge the cities data
            else:
                print(f"Warning: 'cities' key not found in {file_path}")
    else:
        print(f"Error: File {file_path} does not exist.")

# Create merged JSON files for each prefix
for prefix, cities in grouped_cities.items():
    merged_data = {"cities": cities}
    
    # Output file path based on the prefix
    output_file = os.path.join(r"C:\Users\Admin\Desktop\OP", f"{prefix}_merged.json")
    
    # Write the merged cities data to a new file
    with open(output_file, 'w') as outfile:
        json.dump(merged_data, outfile, indent=4)
    
    print(f"Merged cities data for {prefix} has been saved to {output_file}")
