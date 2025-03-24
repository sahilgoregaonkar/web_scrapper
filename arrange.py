import os
import json
from collections import defaultdict

def merge_building_codes(city_folders):
    # Dictionary to store merged data by filename (key)
    merged_files = defaultdict(list)

    # Loop through each category folder
    for folder in city_folders:
        if os.path.isdir(folder):  # Ensure the folder exists
            # Traverse the files in this folder
            for filename in os.listdir(folder):
                if filename.endswith(".json"):
                    file_path = os.path.join(folder, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        # Add the content of the file to the merged files dictionary by filename
                        merged_files[filename].append(data)
        else:
            print(f"Warning: Folder {folder} does not exist or is not a directory.")

    # Prepare the final output structure
    final_data = {"cities": []}

    # For each file with matching names, merge the data
    for filename, data_list in merged_files.items():
        # Assume each entry in data_list corresponds to a different category's building code data
        combined_city_data = {"name": filename, "buildingCodes": []}

        for data in data_list:
            if "cities" in data:
                for city in data["cities"]:
                    combined_city_data["buildingCodes"].extend(city.get("buildingCodes", []))

        final_data["cities"].append(combined_city_data)

    # Save the combined data into a new JSON file
    output_file = os.path.join("output", "combined_building_codes.json")
    os.makedirs("output", exist_ok=True)

    with open(output_file, "w") as output:
        json.dump(final_data, output, indent=4)

# List of folder paths to each category (building code data for different cities)
city_folders = [
     r"C:\Users\Admin\Desktop\New York\Building Code (IBC)\Cities",  # Replace with your actual paths
    r"C:\Users\Admin\Desktop\New York\Energy Conservation Code (IECC)\Cities",
    r"C:\Users\Admin\Desktop\New York\Existing Building Code (IEBC)\Cities",
    r"C:\Users\Admin\Desktop\New York\Fire Code (IFC)\Cities",
    r"C:\Users\Admin\Desktop\New York\Fuel Gas Code (IFGC)\Cities",
    r"C:\Users\Admin\Desktop\New York\Mechanical Code (IMC)\Cities",
    r"C:\Users\Admin\Desktop\New York\Plumbing Code (IPC)\Cities",
    r"C:\Users\Admin\Desktop\New York\Property Maintenance Code (IPMC)\Cities",
    r"C:\Users\Admin\Desktop\New York\Residential Code (IRC)\Cities"
]

merge_building_codes(city_folders)
