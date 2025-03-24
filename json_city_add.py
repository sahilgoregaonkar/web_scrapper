import json
import os

# Path to the input JSON file and city names text file
json_file_path = r"C:\Users\Admin\Desktop\web-scrapper\city_template.json"
city_names_file_path = r"C:\Users\Admin\Desktop\New_York_Cities.txt"
output_folder = r"C:\Users\Admin\Desktop\Json_Output"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the list of city names from the text file
with open(city_names_file_path, "r", encoding="utf-8") as file:
    city_names = [line.strip() for line in file if line.strip()]

# Load the JSON file with utf-8 encoding
with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Update the JSON and save a new file for each city
for city in city_names:
    data['name'] = city  # Replace the 'name' field with the city name
    output_file_path = os.path.join(output_folder, f"{city}.json")
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, indent=4, ensure_ascii=False)

print(f"Generated {len(city_names)} JSON files in the '{output_folder}' folder.")
