import json
import re  # To clean up unwanted characters

# Function to load the JSON file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

# Function to save the updated JSON back to the file
def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)  # ensure_ascii=False to keep non-ASCII characters

# Static list of queries (chapters and appendices)
queries = [
    
   "-ny-chapter-1-scope-and-administration",
    "chapter-2-definitions",
    "chapter-3-general-regulations",
    "chapter-4-gas-piping-installations",
    "chapter-5-chimneys-and-vents",
    "chapter-6-specific-appliances",
    "chapter-7-gaseous-hydrogen-systems",
    "chapter-8-referenced-standards",
    "appendix-a-sizing-and-capacities-of-gas-piping",
    "appendix-b-sizing-of-venting-systems-serving-appliances-equipped-with-draft-hoods-category-i-appliances-and-appliances-listed-for-use-with-type-b-vents",
    "appendix-d-recommended-procedure-for-safety-inspection-of-an-existing-appliance-installation",
    
]

# Function to clean up the section and subsection names for valid URLs
def clean_name(name):
    """Remove everything except digits and periods (to clean up section/subsection numbering)."""
    name = re.sub(r'[^0-9.]', '', name)  # Remove everything except digits and periods
    return name

# Function to create the URLs
def create_url(base_url, query, name, item_type):
    """Generate a URL for chapter, section, or subsection based on its type."""
    
    # Check if the query is related to an appendix (contains "appendix")
    if "appendix" in query.lower():  # For Appendices
        # Extract the appendix identifier (the letter) from the query (e.g., "appendix-a-employee-qualifications" -> "a")
        appendix_identifier = query.split("-")[1].upper()  # This should give us "A", "B", "I" etc.
        if not appendix_identifier:
            raise ValueError(f"Invalid appendix identifier: {query}")
        
        #print("Appendix",appendix_identifier)
        
        # Handle the appendix format
        if item_type == "chapter":
            # Create URL for the appendix chapter (base URL)
            return f"{base_url}#NYSFGC2020P1_Appx{appendix_identifier}"

        # Handle section format within appendix (e.g., SecA101.1)
        if item_type == "section":
            section_number = clean_name(name)  # Clean section number
            return f"{base_url}#NYSFGC2020P1_Appx{appendix_identifier}_Sec{appendix_identifier}{section_number}"

        # Handle subsection format within appendix sections
        if item_type == "subsection":
            section_number = clean_name(name.split(".")[0])  # Section part of subsection
            subsection_number = clean_name(name.split(".")[1])  # Subsection part
            return f"{base_url}#NYSFGC2020P1_Appx{appendix_identifier}_Sec{appendix_identifier}{section_number}.{subsection_number}"

    # Extract chapter number for numbered chapters (e.g., "chapter-1-scope-and-administration" -> "1")
    chapter_number = ''.join(filter(str.isdigit, query))  # Extract digits from query
    if not chapter_number:
        raise ValueError(f"Invalid chapter name or query: {query}")
    
    chapter_prefix = f"Ch{int(chapter_number):02d}"  # Format chapter number as Ch01, Ch02, etc.

    # Handle the chapter format
    if item_type == "chapter":
        return f"{base_url}#NYSFGC2020P1_{chapter_prefix}"

    # Handle the section format for numbered chapters
    if item_type == "section":
        section_number = clean_name(name)  # Clean up to get only the numeric section part
        return f"{base_url}#NYSFGC2020P1_{chapter_prefix}_Sec{section_number}"

    # Handle the subsection format for numbered chapters
    if item_type == "subsection":
        # Extract the section number and subsection number
        section_number = ''.join(filter(str.isdigit, name.split(".")[0]))  # Get section number
        subsection_number = clean_name(name.split(".")[1])  # Get digits after the dot (subsection)
        return f"{base_url}#NYSFGC2020P1_{chapter_prefix}_Sec{section_number}.{subsection_number}"

    # If an unknown item_type is encountered, raise an error
    raise ValueError(f"Unknown item type: {item_type}")

# Function to update URLs in the loaded JSON data
def update_urls(data, queries):
    """Update the URLs in the data structure."""
    for query in queries:
        # Define the base URL for this chapter or appendix
        base_url = f"https://codes.iccsafe.org/content/NYSFGC2020P1/{query}"

        # Iterate over the data (each chapter or appendix)
        for chapter_data in data:  # Loop through chapters or appendices in the JSON
            
            chapter_title = chapter_data["chapter"].upper()  # Capitalize chapter name for comparison
            
            if "[NY]" in chapter_data["chapter"]:
                print(f"Removing '[NY]' from chapter title: {chapter_data['chapter']}")
                chapter_data["chapter"] = chapter_data["chapter"].replace("[NY]", "").strip()
                
                

            # Ensure we're only working with appendices or chapters
            if "APPENDIX" in chapter_title and query.lower().startswith("appendix") and chapter_title.split(" ")[1].lower() == query.split("-")[1] :
                # Extract appendix identifier (e.g., "A" from "APPENDIX A")
                appendix_identifier = re.sub(r"[^A-Za-z]", "", chapter_data["chapter"]).upper()
                print(f"Updating URLs for appendix {chapter_data['chapter']} using query: {query}")
                if chapter_title.split(" ")[1].lower() == query.split("-")[1]:
                    print("Matching",chapter_title,"  query",query)
                
                # Update the chapter URL for the appendix
                chapter_url = create_url(base_url, query, chapter_data["chapter"], "chapter")
                chapter_data["chapter_url"] = chapter_url

                # Loop through sections and update their URLs (if applicable)
                for section in chapter_data.get("sections", []):
                    section_url = create_url(base_url, query, section["section"], "section")
                    section["section_url"] = section_url

                    # Loop through subsections and update their URLs (if applicable)
                    for subsection in section.get("subsections", []):
                        subsection_url = create_url(base_url, query, subsection["title"], "subsection")
                        subsection["subsection_url"] = subsection_url

            # Also update URLs for numbered chapters
            elif "CHAPTER" in chapter_title and query.lower().startswith("chapter") :
                chapter_identifier = re.sub(r"[^0-9]", "", query)
                chapter_number = re.sub(r"[^0-9]", "", chapter_data["chapter"])

                if chapter_identifier != chapter_number:
                    print(f"Skipping chapter {chapter_data['chapter']} as it does not match {query}")
                    continue

                # Update the chapter URL for the numbered chapter
                chapter_url = create_url(base_url, query, chapter_data["chapter"], "chapter")
                chapter_data["chapter_url"] = chapter_url

                # Loop through sections and update their URLs (if applicable)
                for section in chapter_data.get("sections", []):
                    section_url = create_url(base_url, query, section["section"], "section")
                    section["section_url"] = section_url

                    # Loop through subsections and update their URLs (if applicable)
                    for subsection in section.get("subsections", []):
                        subsection_url = create_url(base_url, query, subsection["title"], "subsection")
                        subsection["subsection_url"] = subsection_url

    return data

# Main function to process the JSON file and update it
def process_json_file(file_path):
    # Load the JSON data
    data = load_json(file_path)

    # Update the URLs in the data
    updated_data = update_urls(data, queries)

    # Save the updated data back to the file
    save_json(file_path, updated_data)
    print("The JSON file has been updated with new URLs.")

# Example usage
file_path = r"C:\Users\Admin\Desktop\web-scrapper\output.json"  # Replace with the actual path to your JSON file
process_json_file(file_path)
