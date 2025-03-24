
import os
import shutil

# List of the 9 different "Cities" folder paths
cities_folders = [
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

# Output folder path
output_path = r"C:\Users\Admin\Desktop\Club"  # Replace with where you want the city folders

# Ensure the output directory exists
os.makedirs(output_path, exist_ok=True)

# Iterate over the list of cities folder paths
for cities_folder_path in cities_folders:
    # Check if the current folder exists and is a directory
    if os.path.exists(cities_folder_path) and os.path.isdir(cities_folder_path):
        print(f"Processing folder: {cities_folder_path}")  # Debug: show which folder is being processed
        
        # Iterate over JSON files in the "Cities" folder
        for file_name in os.listdir(cities_folder_path):
            if file_name.endswith(".json"):  # Process only JSON files
                print(f"Found file: {file_name}")  # Debug: show which file is being processed
                
                # Extract city name from the file name (assumed to be the city)
                city_name = os.path.splitext(file_name)[0]
                city_output_folder = os.path.join(output_path, city_name)
                
                # Ensure the city folder exists in the output path
                os.makedirs(city_output_folder, exist_ok=True)
                
                # Copy the JSON file to the city folder
                source_file = os.path.join(cities_folder_path, file_name)
                destination_file = os.path.join(city_output_folder, file_name)
                
                # Check if file already exists to avoid overwriting
                if not os.path.exists(destination_file):
                    shutil.copy(source_file, destination_file)
                else:
                    print(f"File already exists: {file_name}")  # Debug: indicate if file already exists

print("All files have been organized by city!")




