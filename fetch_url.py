from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# Setup the Chrome WebDriver (headless mode)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Optional: Run in headless mode (no GUI)
driver = webdriver.Chrome(options=options)

# Step 1: Load the current output.json to get sections and subsections
with open('output.json', 'r', encoding='utf-8') as f:
    output_data = json.load(f)

# Step 2: Iterate over each section and fetch URLs
for item in output_data:
    section_title = item["section"]
    
    # Step 3: Create the base URL for the section (adjust to match URL pattern)
    query = section_title.lower().replace(" ", "-")
    section_url = f"https://codes.iccsafe.org/content/NYNYCBC2022P1/{query}"
    
    # Update the section URL in the output_data
    item["section_url"] = section_url

    # Step 4: Iterate over subsections and fetch URLs
    for subsection in item["subsections"]:
        subsection_title = subsection["title"]
        subsection_url = None

        # Construct the subsection URL based on its title
        # Create a subsection ID using a numbering scheme similar to the example URLs
        # For example, if subsection is 115.1, it will become #NYNYCBC2022P1_Ch01_Sec115.1
        subsection_number = subsection_title.split('.')[0]  # Extract the main number before the first dot
        subsection_id = f"NYNYCBC2022P1_{query.replace('-', '')}_Sec{subsection_number}"

        # Build the full URL with anchor
        subsection_url = f"{section_url}#{subsection_id}"

        # Update the subsection URL in the output_data
        subsection["subsection_url"] = subsection_url

# Step 5: Write the updated data back to output.json
with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, indent=4, ensure_ascii=False)

print("URLs have been successfully added to output.json")

# Close the WebDriver after processing
driver.quit()
