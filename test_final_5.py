from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import json
import os
import time

# Initialize Selenium WebDriver (assume Chrome here)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)

driver = webdriver.Chrome(options=options)

output_data = []  # List to hold the data for all chapters, sections, and subsections

# Loop through all HTML files in the "data" directory
for file in os.listdir("data"):
    if file.endswith(".html"):  # Ensure only HTML files are processed
        try:
            file_path = f"file:///{os.path.abspath(f'data/{file}')}"  # Local file URL
            driver.get(file_path)  # Load the local HTML file in the browser

            # Allow the page to load for a moment (adjust as needed)
            time.sleep(2)

            # Get the page source and pass it to BeautifulSoup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Track processed chapters and sections to avoid duplicates
            processed_chapters = set()
            processed_sections = set()

            # Process chapters identified by the data-chapter-title attribute
            for chapter_tag in soup.find_all(attrs={"data-chapter-title": True}):  
                chapter_title = chapter_tag.get("data-chapter-title").strip()

                # Skip if chapter has already been processed
                if chapter_title in processed_chapters:
                    continue
                processed_chapters.add(chapter_title)

                # Initialize the chapter structure
                chapter_data = {
                    "chapter": chapter_title,
                    "sections": []
                }

                # Try to get the chapter URL (use Selenium to extract it)
                chapter_url = None
                try:
                    # Find the first preceding <a> tag for the chapter
                    link_tag = chapter_tag.find_element(By.XPATH, './/preceding::a[1]')
                    if link_tag and link_tag.get_attribute('href'):
                        chapter_url = link_tag.get_attribute('href').strip()
                except Exception as e:
                    print(f"Error extracting URL for chapter {chapter_title}: {e}")

                # Now, we use BeautifulSoup to process sections and subsections within the chapter
                for tag in chapter_tag.find_all_next(['h1', 'p']):
                    if tag.name == 'h1' and tag.get('data-chapter-title'):  # Found next chapter
                        break
                    if tag.name == 'h1' and 'level1' in tag.get('class', []):  # It's a section
                        section_number = tag.find('span', class_='section_number').get_text(strip=True)
                        section_title = tag.find('span', class_='level1_title').get_text(strip=True)
                        full_section_title = f"SECTION BC {section_number} {section_title}"  # Full section label: "SECTION BC 101 GENERAL"

                        # Skip if section has already been processed
                        if full_section_title in processed_sections:
                            continue
                        processed_sections.add(full_section_title)

                        # Initialize the section structure
                        section_data = {
                            "section": full_section_title,
                            "subsections": []
                        }

                        # Try to get the section URL (use Selenium to extract it)
                        section_url = None
                        try:
                            section_link_tag = tag.find_element(By.XPATH, './/preceding::a[1]')
                            if section_link_tag and section_link_tag.get_attribute('href'):
                                section_url = section_link_tag.get_attribute('href').strip()
                        except Exception as e:
                            print(f"Error extracting URL for section {full_section_title}: {e}")

                        # Process subsections for this section
                        subsections_found = False
                        for subsection_tag in tag.find_all_next(['h1', 'p']):
                            if subsection_tag.name == 'h1' and 'level1' in subsection_tag.get('class', []):  # Found next section
                                break
                            if subsection_tag.name == 'h1' and 'level2' in subsection_tag.get('class', []):  # It's a subsection
                                subsection_title = subsection_tag.get_text(strip=True)
                                subsection_content = ""

                                # Find the next <p> tag for the subsection content
                                next_p_tag = subsection_tag.find_next('p')
                                if next_p_tag:
                                    subsection_content = next_p_tag.get_text(strip=True)

                                # Try to get the subsection URL (use Selenium to extract it)
                                subsection_url = None
                                try:
                                    subsection_link_tag = subsection_tag.find_element(By.XPATH, './/preceding::a[1]')
                                    if subsection_link_tag and subsection_link_tag.get_attribute('href'):
                                        subsection_url = subsection_link_tag.get_attribute('href').strip()
                                except Exception as e:
                                    print(f"Error extracting URL for subsection {subsection_title}: {e}")

                                # Add subsection data
                                subsection_data = {
                                    "title": subsection_title,
                                    "content": subsection_content,
                                    "subsection_url": subsection_url,
                                    "subsubsections": []  # Placeholder for deeper subsections
                                }

                                # Look for tables and other subsections (e.g., level 3, level 4)
                                for deeper_tag in subsection_tag.find_all_next(['h1', 'p', 'figure']):
                                    if deeper_tag.name == 'h1' and 'level2' in deeper_tag.get('class', []):  # Found next subsection
                                        break
                                    if deeper_tag.name == 'h1' and 'level3' in deeper_tag.get('class', []):  # It's a deeper subsection (level3)
                                        deeper_subsection_title = deeper_tag.get_text(strip=True)
                                        deeper_subsection_content = ""

                                        # Find the next <p> tag for the deeper subsection content
                                        next_p_tag = deeper_tag.find_next('p')
                                        if next_p_tag:
                                            deeper_subsection_content = next_p_tag.get_text(strip=True)

                                        # Add deeper subsection
                                        subsection_data["subsubsections"].append({
                                            "title": deeper_subsection_title,
                                            "content": deeper_subsection_content,
                                            "subsubsection_url": None
                                        })

                                    # Look for tables within <figure> tags
                                    if deeper_tag.name == 'figure' and 'table' in deeper_tag.get('class', []):
                                        # Extract table title
                                        table_title = deeper_tag.find('p', class_='table_title').get_text(strip=True) if deeper_tag.find('p', class_='table_title') else "No Title"
                                        
                                        # Extract table rows and cells
                                        table_rows = deeper_tag.find_all('tr')
                                        table_data = []
                                        for row in table_rows:
                                            row_data = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                                            table_data.append(row_data)

                                        # Add table as a subsubsection under the current subsection
                                        subsection_data["subsubsections"].append({
                                            "title": table_title,
                                            "content": "Table Data",
                                            "table_data": table_data,
                                        })
                                    
                                    # Handle level 4 and level 5 subsections
                                    if deeper_tag.name == 'h1' and 'level4' in deeper_tag.get('class', []):  # It's a level 4 subsection
                                        level4_subsection_title = deeper_tag.get_text(strip=True)
                                        level4_subsection_content = ""

                                        # Find the next <p> tag for the level4 content
                                        next_p_tag = deeper_tag.find_next('p')
                                        if next_p_tag:
                                            level4_subsection_content = next_p_tag.get_text(strip=True)

                                        # Try to get the level4 subsection URL
                                        level4_subsection_url = None
                                        try:
                                            level4_link_tag = deeper_tag.find_element(By.XPATH, './/preceding::a[1]')
                                            if level4_link_tag and level4_link_tag.get_attribute('href'):
                                                level4_subsection_url = level4_link_tag.get_attribute('href').strip()
                                        except Exception as e:
                                            print(f"Error extracting URL for level 4 subsection {level4_subsection_title}: {e}")

                                        # Add level 4 subsection to the current subsection
                                        subsection_data["subsubsections"].append({
                                            "title": level4_subsection_title,
                                            "content": level4_subsection_content,
                                            "subsubsection_url": level4_subsection_url
                                        })

                                    # Handle level 5 subsections
                                    if deeper_tag.name == 'h1' and 'level5' in deeper_tag.get('class', []):  # It's a level 5 subsection
                                        level5_subsection_title = deeper_tag.get_text(strip=True)
                                        level5_subsection_content = ""

                                        # Find the next <p> tag for the level5 content
                                        next_p_tag = deeper_tag.find_next('p')
                                        if next_p_tag:
                                            level5_subsection_content = next_p_tag.get_text(strip=True)

                                        # Try to get the level5 subsection URL
                                        level5_subsection_url = None
                                        try:
                                            level5_link_tag = deeper_tag.find_element(By.XPATH, './/preceding::a[1]')
                                            if level5_link_tag and level5_link_tag.get_attribute('href'):
                                                level5_subsection_url = level5_link_tag.get_attribute('href').strip()
                                        except Exception as e:
                                            print(f"Error extracting URL for level 5 subsection {level5_subsection_title}: {e}")

                                        # Add level 5 subsection to the current subsection
                                        subsection_data["subsubsections"].append({
                                            "title": level5_subsection_title,
                                            "content": level5_subsection_content,
                                            "subsubsection_url": level5_subsection_url
                                        })


                                # Add the subsection data to the section if there were subsections
                                section_data["subsections"].append(subsection_data)
                                subsections_found = True

                        # Only append section data if subsections were found
                        if subsections_found:
                            section_data["section_url"] = section_url
                            chapter_data["sections"].append(section_data)

                # Only append chapter data if sections were found
                if chapter_data["sections"]:
                    chapter_data["chapter_url"] = chapter_url
                    output_data.append(chapter_data)

        except Exception as e:
            print(f"Error processing {file}: {e}")

# Write the output data to a JSON file
try:
    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, indent=4, ensure_ascii=False)
    print("Data has been successfully written to output.json")
except Exception as e:
    print(f"Error writing to output.json: {e}")

driver.quit()  # Close the WebDriver
