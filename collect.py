from bs4 import BeautifulSoup
import os
import json

output_data = []  # List to hold the data for all files

# Loop through all HTML files in the "data" directory
for file in os.listdir("data"):
    if file.endswith(".html"):  # Ensure only HTML files are processed
        try:
            with open(f"data/{file}", "r", encoding="utf-8") as f:
                html_doc = f.read()
            
            soup = BeautifulSoup(html_doc, 'html.parser')
            
            # Process sections (level1 tags)
            for level1_tag in soup.find_all('h1', class_='level1'):
                section_title = level1_tag.get_text(strip=True)
                
                # Initialize the section structure
                section_data = {
                    "section": section_title,
                    "subsections": []
                }
                
                # Find all subsections after this section
                subsections_found = False
                for tag in level1_tag.find_all_next(['h1', 'p']):
                    if tag.name == 'h1' and tag.get('class') == ['level1']:  # Found next section
                        break
                    if tag.name == 'h1' and tag.get('id'):  # It's a subsection
                        title_id = tag['id'].strip()
                        title_text = tag.get_text(strip=True)
                        
                        # Find corresponding <p> tag for this subsection
                        corresponding_p_tag = soup.find('p', id=lambda x: x and x.startswith(title_id))
                        content_text = corresponding_p_tag.get_text(strip=True) if corresponding_p_tag else "No content"
                        
                        # Add subsection to the section
                        section_data["subsections"].append({
                            "title": title_text,
                            "content": content_text
                        })
                        subsections_found = True

                # Add section data to the output list only if subsections were found
                if subsections_found:
                    output_data.append(section_data)

        except Exception as e:
            print(f"Error processing {file}: {e}")

# Write the output data to a JSON file
try:
    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, indent=4, ensure_ascii=False)
    print("Data has been successfully written to output.json")
except Exception as e:
    print(f"Error writing to output.json: {e}")
