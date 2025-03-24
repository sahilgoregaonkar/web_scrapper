import os
import shutil
from collections import defaultdict

def gather_files(folders, output_folder):
    # Create a dictionary to track files by their name
    file_dict = defaultdict(list)

    # Iterate through all the folders and collect files
    for folder in folders:
        if not os.path.exists(folder):
            print(f"Warning: {folder} does not exist.")
            continue

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                file_dict[filename].append(file_path)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through the dictionary and move files with the same name
    for filename, file_paths in file_dict.items():
        if len(file_paths) == 7:  # Only move files if they exist in all 9 folders
            for idx, file_path in enumerate(file_paths):
                new_file_name = f"{idx + 1}_{filename}"  # Add an index to distinguish them
                new_file_path = os.path.join(output_folder, new_file_name)
                shutil.copy(file_path, new_file_path)
                print(f"Copied {filename} from {file_path} to {new_file_path}")
        else:
            print(f"File {filename} is missing from some folders.")

# Example usage:
folders = [
    r"C:\Users\Admin\Desktop\Building_Codes\Ohio\Building Code (IBC)\Cities",  # Replace with your actual paths
    r"C:\Users\Admin\Desktop\Building_Codes\Ohio\Energy Code (IECC)\Cities",
    r"C:\Users\Admin\Desktop\Building_Codes\Ohio\Existing Building Code (IEBC)\Cities",
    r"C:\Users\Admin\Desktop\Building_Codes\Ohio\Fire Code (IFC)\Cities",
    r"C:\Users\Admin\Desktop\Building_Codes\Ohio\Mechanical Code (IMC)\Cities",
    r"C:\Users\Admin\Desktop\Building_Codes\Ohio\Plumbing Code (IPC)\Cities",
    r"C:\Users\Admin\Desktop\Building_Codes\Ohio\Residential Code (IRC)\Cities"
    
]

output_folder = r"C:\Users\Admin\Desktop\Indexed"
gather_files(folders, output_folder)
