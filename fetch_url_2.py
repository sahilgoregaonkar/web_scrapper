import json
import os

# Step 1: Specify the path to your output.json file
json_file_path = r'C:\Users\Admin\Desktop\web-scrapper\output.json'  # Update this path as required

# Ensure the file exists before processing
if not os.path.exists(json_file_path):
    print(f"File {json_file_path} does not exist.")
    exit()

# Step 2: Load the data from the output.json file
with open(json_file_path, 'r', encoding='utf-8') as f:
    output_data = json.load(f)

# Step 3: Iterate over each chapter to generate chapter URLs and section URLs
for chapter in output_data["chapters"]:
    chapter_title = chapter["chapter"]
    
    # Generate the chapter slug for the URL (e.g., "chapter-1-administration")
    chapter_slug = chapter_title.lower().replace(" ", "-").replace("chapter", "chapter-")
    chapter_url = f"https://codes.iccsafe.org/content/NYNYCBC2022P1/{chapter_slug}"
    
    # Add chapter URL to the chapter data
    chapter["chapter_url"] = chapter_url

    # Step 4: Iterate over each section and generate URLs
    for section in chapter["sections"]:
        section_title = section["section"]
        
        # Extract the section number (e.g., 101 from "SECTION BC 101 GENERAL")
        section_number = section_title.split(" ")[2]  # Assumes section number is the 3rd word in "SECTION BC 101 GENERAL"
        
        # Generate section URL based on the chapter URL
        section_url = f"{chapter_url}#NYNYCBC2022P1_Ch01_Sec{section_number}"
        section["section_url"] = section_url

        # Step 5: Iterate over subsections and generate URLs
        for subsection in section["subsections"]:
            subsection_title = subsection["title"]
            
            # Extract the subsection number (e.g., 101.1 from "101.1 Title")
            subsection_number = subsection_title.split(" ")[0]  # Extract before the first space, like 101.1
            subsection_id = f"NYNYCBC2022P1_{chapter_slug.replace('-', '')}_Sec{subsection_number}"

            # Generate subsection URL with anchor
            subsection_url = f"{section_url}#{subsection_id}"
            subsection["subsection_url"] = subsection_url

# Step 6: Save the updated data back to output.json
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, indent=4, ensure_ascii=False)

print("URLs have been successfully added to output.json")
