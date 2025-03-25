import json

def correct_json_structure(data):
    # Check if data is a dictionary at the top level
    if not isinstance(data, dict):
        print("Error: The input data is not a dictionary as expected.")
        return data  # Return the original data if it's not a dictionary
    
    corrected_sections = []
    current_section = None
    
    # Add chapter_url at the chapter level
    corrected_data = {
        "chapter": data.get("chapter", ""),
        "chapter_url": None,  # Add chapter_url here
        "sections": []
    }
    
    sections = data.get("sections", [])
    
    # Check if 'sections' is a list
    if not isinstance(sections, list):
        print("Error: The 'sections' key is not a list as expected.")
        return data  # Return the original data if 'sections' is not a list
    
    # Process sections and subsections
    for item in sections:
        # Ensure each item is a dictionary with the expected structure
        if not isinstance(item, dict):
            print(f"Warning: Skipping invalid section format: {item}")
            continue
        
        section_title = item.get("section", "").strip()
        
        # If the section contains "SECTION", create a new section
        if "SECTION" in section_title:
            # If we already have a current section, append it to the list
            if current_section:
                corrected_sections.append(current_section)
            
            # Start a new section with "section_url": null
            current_section = {
                "section": section_title,
                "section_url": None,  # Add section_url here
                "subsections": []
            }
            
            # Process the subsections under this section
            subsections = item.get("subsections", [])
            if isinstance(subsections, list):
                for subsection in subsections:
                    # Ensure subsection is a dictionary
                    if isinstance(subsection, dict):
                        current_section["subsections"].append({
                            "title": subsection.get("title"),
                            "content": subsection.get("content"),
                            "subsection_url": subsection.get("subsection_url")
                        })
                    else:
                        print(f"Warning: Skipping invalid subsection format: {subsection}")
    
    # Add the last section if exists
    if current_section:
        corrected_sections.append(current_section)
    
    # Assign the corrected sections list to the final structure
    corrected_data["sections"] = corrected_sections
    
    # Return the corrected structure
    return corrected_data

def process_local_json(file_path):
    try:
        # Open the JSON file to read its content
        with open(file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)
        
        # Correct the JSON structure
        corrected_data = correct_json_structure(data)
        
        # Write the corrected JSON back to the file
        with open(file_path, 'w', encoding="utf-8") as json_file:
            json.dump(corrected_data, json_file, indent=4, ensure_ascii=False)
        
        print(f"Data has been successfully written to {file_path}")

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage: Replace this with the actual file path of your JSON
process_local_json(r"C:\Users\Admin\Desktop\web-scrapper\output.json")












