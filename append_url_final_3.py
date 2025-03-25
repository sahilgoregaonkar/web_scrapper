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
     "appendix-o-performance-based-application",
]

# Function to clean up the section and subsection names for valid URLs
def clean_name(name):
    """Remove everything except digits and periods (to clean up section/subsection numbering)."""
    name = re.sub(r'[^0-9.]', '', name)  # Remove everything except digits and periods
    return name

# Function to update URLs in the loaded JSON data
def update_urls(data, queries):
    """Update the URLs in the data structure."""
    for query in queries:
        # Define the base URL for this chapter or appendix
        base_url = f"https://codes.iccsafe.org/content/CABC2022P4/{query}"

        # Iterate over the data (each chapter or appendix)
        for chapter_data in data:  # Loop through chapters or appendices in the JSON
            chapter_title = chapter_data["chapter"].upper()  # Capitalize chapter name for comparison

            if "[NY]" in chapter_data["chapter"]:
                print(f"Removing '[NY]' from chapter title: {chapter_data['chapter']}")
                chapter_data["chapter"] = chapter_data["chapter"].replace("[NY]", "").strip()

            # Update URLs for appendices
            if "APPENDIX" in chapter_title and query.lower().startswith("appendix") and chapter_title.split(" ")[1].lower() == query.split("-")[1]:
                appendix_identifier = re.sub(r"[^A-Za-z]", "", chapter_data["chapter"]).upper()
                print(f"Updating URLs for appendix {chapter_data['chapter']} using query: {query}")
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

                        # Loop through subsubsections (if present) and update their URLs
                        for subsubsection in subsection.get("subsubsections", []):
                            subsubsection_url = create_url(base_url, query, subsubsection["title"], "subsubsection")
                            subsubsection["subsubsection_url"] = subsubsection_url

            # Also update URLs for numbered chapters
            elif "CHAPTER" in chapter_title and query.lower().startswith("chapter"):
                chapter_identifier = re.sub(r"[^0-9]", "", query)
                chapter_number = re.sub(r"[^0-9]", "", chapter_data["chapter"])

                if chapter_identifier != chapter_number:
                    print(f"Skipping chapter {chapter_data['chapter']} as it does not match {query}")
                    continue

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

                        # Loop through subsubsections (if present) and update their URLs
                        for subsubsection in subsection.get("subsubsections", []):
                            subsubsection_url = create_url(base_url, query, subsubsection["title"], "subsubsection")
                            subsubsection["subsubsection_url"] = subsubsection_url

    return data

# Function to create the URLs
def create_url(base_url, query, name, item_type):
    """Generate a URL for chapter, section, subsection, or subsubsection based on its type."""
    
    # Check if the query is related to an appendix (contains "appendix")
    if "appendix" in query.lower():  # For Appendices
        appendix_identifier = query.split("-")[1].upper()  # This should give us "A", "B", "I" etc.
        if not appendix_identifier:
            raise ValueError(f"Invalid appendix identifier: {query}")
        
        if item_type == "chapter":
            return f"{base_url}#CABC2022P4_Appx{appendix_identifier}"

        if item_type == "section":
            section_number = clean_name(name)
            return f"{base_url}#CABC2022P4_Appx{appendix_identifier}_Sec{appendix_identifier}{section_number}"

        if item_type == "subsection":
            parts = name.split(".")
            section_number = clean_name(parts[0])  # Section part of subsection
            subsection_number = clean_name(parts[1]) if len(parts) > 1 else ''
            return f"{base_url}#CABC2022P4_Appx{appendix_identifier}_Sec{appendix_identifier}{section_number}.{subsection_number}"

        if item_type == "subsubsection":
            parts = name.split(".")
            section_number = clean_name(parts[0])  
            subsection_number = clean_name(parts[1]) if len(parts) > 1 else ''
            subsubsection_number = clean_name(parts[2]) if len(parts) > 2 else ''
            return f"{base_url}#CABC2022P4_Appx{appendix_identifier}_Sec{appendix_identifier}{section_number}.{subsection_number}.{subsubsection_number}"

    chapter_number = ''.join(filter(str.isdigit, query))
    if not chapter_number:
        raise ValueError(f"Invalid chapter name or query: {query}")
    
    chapter_prefix = f"Ch{int(chapter_number):02d}"

    if item_type == "chapter":
        return f"{base_url}#CABC2022P4_{chapter_prefix}"

    if item_type == "section":
        section_number = clean_name(name)
        return f"{base_url}#CABC2022P4_{chapter_prefix}_Sec{section_number}"

    if item_type == "subsection":
        parts = name.split(".")
        section_number = ''.join(filter(str.isdigit, parts[0]))  
        subsection_number = clean_name(parts[1]) if len(parts) > 1 else ''
        return f"{base_url}#CABC2022P4_{chapter_prefix}_Sec{section_number}.{subsection_number}"

    if item_type == "subsubsection":
        parts = name.split(".")
        section_number = ''.join(filter(str.isdigit, parts[0]))  
        subsection_number = clean_name(parts[1]) if len(parts) > 1 else ''
        subsubsection_number = clean_name(parts[2]) if len(parts) > 2 else ''
        return f"{base_url}#CABC2022P4_{chapter_prefix}_Sec{section_number}.{subsection_number}.{subsubsection_number}"

    raise ValueError(f"Unknown item type: {item_type}")

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
