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
    
   "chapter-1-scope-and-administration",
    "chapter-2-definitions",
    "chapter-3-occupancy-classification-and-use",
    "chapter-4-special-detailed-requirements-based-on-occupancy-and-use",
    "chapter-5-general-building-heights-and-areas",
    "chapter-6-types-of-construction",
    "chapter-7-fire-and-smoke-protection-features",
    "chapter-7a-sfm-materials-and-construction-methods-for-exterior-wildfire-exposure",
    "chapter-8-interior-finishes",
    "chapter-9-fire-protection-and-life-safety-systems",
    "chapter-10-means-of-egress",
#     "chapter-11a-housing-accessibility",
#     "chapter-11b-accessibility-to-public-buildings-public-accommodations-commercialbuildings-and-public-housing",
#     "chapter-12-interior-environment",
#     "chapter-13-energy-efficiency",
#     "chapter-14-exterior-walls",
#     "chapter-15-roof-assemblies-and-rooftop-structures",
#     "chapter-16-structural-design",
#     "chapter-16a-structural-design",
#     "chapter-17-special-inspections-and-tests",
#     "chapter-17a-special-inspections-and-tests",
#     "chapter-18-soils-and-foundations",
#     "chapter-18a-soils-and-foundations",
#     "chapter-19-concrete",
#     "chapter-19a-concrete",
#     "chapter-20-aluminum",
#     "chapter-21-masonry",
#     "chapter-21a-masonry",
#     "chapter-22-steel",
#     "chapter-22a-steel",
#     "chapter-23-wood",
#     "chapter-24-glass-and-glazing",
#     "chapter-25-gypsum-board-gypsum-panel-products-and-plaster",
#     "chapter-26-plastic",
#     "chapter-27-electrical",
#     "chapter-28-mechanical-systems",
#     "chapter-29-plumbing-systems",
#     "chapter-30-elevators-and-conveying-systems",
#     "chapter-31-special-construction",
#     "chapter-31b-dph-public-pools",
#     "chapter-31c-dph-radiation",
#     "chapter-31d-dph-food-establishments",
#     "chapter-31f-slc-marine-oil-terminals",
#     "chapter-32-encroachments-into-the-public-right-of-way",
#     "chapter-33-safeguards-during-construction",
    # "appendix-a-employee-qualifications",
    # "appendix-b-board-of-appeals",
    # "appendix-c-group-u-agricultural-buildings",
    # "appendix-d-fire-districts",
    # "appendix-f-rodentproofing",
    
    # "appendix-g-flood-resistant-construction",
    # "appendix-h-signs",
    # "appendix-i-patio-covers",
    # "appendix-j-grading",
    # "appendix-k-group-r-3-and-group-r-3-1-occupancies-protected-by-the-facilities-of-the-central-valley-flood-protection-plan",
    # "appendix-l-earthquake-recording-instrumentation",
    # "appendix-m-tsunami-generated-flood-hazards",
    # "appendix-n-replicable-buildings",
    # "appendix-o-performance-based-application",
    # "appendix-p-emergency-housing",
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
                # Extract appendix identifier (e.g., "A" from "APPENDIX A")
                appendix_identifier = re.sub(r"[^A-Za-z]", "", chapter_data["chapter"]).upper()
                print(f"Updating URLs for appendix {chapter_data['chapter']} using query: {query}")

                # Update the chapter URL for the appendix
                chapter_url = create_url(base_url, query, chapter_data["chapter"], "chapter")
                chapter_data["chapter_url"] = chapter_url

                # Loop through sections and update their URLs (if applicable)
                if "SECTION" in chapter_title:
                    # Update the section URL
                    section_url = create_url(base_url, query, chapter_data["section"], "section")
                    chapter_data["section_url"] = section_url

                    # Loop through subsections and update their URLs (if applicable)
                    for subsection in chapter_data.get("subsections", []):
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
        # Extract the appendix identifier (the letter) from the query (e.g., "appendix-a-employee-qualifications" -> "a")
        appendix_identifier = query.split("-")[1].upper()  # This should give us "A", "B", "I" etc.
        if not appendix_identifier:
            raise ValueError(f"Invalid appendix identifier: {query}")
        
        # Handle the appendix format
        if item_type == "chapter":
            # Create URL for the appendix chapter (base URL)
            return f"{base_url}#CABC2022P4_Appx{appendix_identifier}"

        # Handle section format within appendix (e.g., SecA101.1)
        if item_type == "section":
            section_number = clean_name(name)  # Clean section number
            return f"{base_url}#CABC2022P4_Appx{appendix_identifier}_Sec{appendix_identifier}{section_number}"

        # Handle subsection format within appendix sections
        if item_type == "subsection":
            section_number = clean_name(name.split(".")[0])  # Section part of subsection
            subsection_number = clean_name(name.split(".")[1])  # Subsection part
            return f"{base_url}#CABC2022P4_Appx{appendix_identifier}_Sec{appendix_identifier}{section_number}.{subsection_number}"

        # Handle subsubsection format
        if item_type == "subsubsection":
            section_number = clean_name(name.split(".")[0])  # Section part of subsubsection
            subsection_number = clean_name(name.split(".")[1])  # Subsection part
            subsubsection_number = clean_name(name.split(".")[2])  # Subsubsection part
            return f"{base_url}#CABC2022P4_Appx{appendix_identifier}_Sec{appendix_identifier}{section_number}.{subsection_number}.{subsubsection_number}"

    # Extract chapter number for numbered chapters (e.g., "chapter-1-scope-and-administration" -> "1")
    chapter_number = ''.join(filter(str.isdigit, query))  # Extract digits from query
    if not chapter_number:
        raise ValueError(f"Invalid chapter name or query: {query}")
    
    chapter_prefix = f"Ch{int(chapter_number):02d}"  # Format chapter number as Ch01, Ch02, etc.

    # Handle the chapter format
    if item_type == "chapter":
        return f"{base_url}#CABC2022P4_{chapter_prefix}"

    # Handle the section format for numbered chapters
    if item_type == "section":
        section_number = clean_name(name)  # Clean up to get only the numeric section part
        return f"{base_url}#CABC2022P4_{chapter_prefix}_Sec{section_number}"

    # Handle the subsection format for numbered chapters
    if item_type == "subsection":
        # Extract the section number and subsection number
        section_number = ''.join(filter(str.isdigit, name.split(".")[0]))  # Get section number
        subsection_number = clean_name(name.split(".")[1])  # Get digits after the dot (subsection)
        return f"{base_url}#CABC2022P4_{chapter_prefix}_Sec{section_number}.{subsection_number}"

    # Handle subsubsection format (if applicable)
    if item_type == "subsubsection":
        section_number = ''.join(filter(str.isdigit, name.split(".")[0]))  # Section part of subsubsection
        subsection_number = clean_name(name.split(".")[1])  # Subsection part
        subsubsection_number = clean_name(name.split(".")[2])  # Subsubsection part
        return f"{base_url}#CABC2022P4_{chapter_prefix}_Sec{section_number}.{subsection_number}.{subsubsection_number}"

    # If an unknown item_type is encountered, raise an error
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