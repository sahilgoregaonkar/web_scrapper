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

output_data = []  # List to hold the data for all sections and subsections

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

            # Process sections (level1 tags)
            for level1_tag in soup.find_all('h1', class_='level1'):
                section_title = level1_tag.get_text(strip=True)

                # Initialize the section structure
                section_data = {
                    "section": section_title,
                    "subsections": []
                }

                # Try to get the section URL (use Selenium to extract it)
                section_url = None
                try:
                    # Find the first preceding <a> tag for the section
                    link_tag = level1_tag.find_element(By.XPATH, './/preceding::a[1]')
                    if link_tag and link_tag.get_attribute('href'):
                        section_url = link_tag.get_attribute('href').strip()
                except Exception as e:
                    print(f"Error extracting URL for section {section_title}: {e}")

                # Now, we use BeautifulSoup to process subsections after this section
                subsections_found = False
                for tag in level1_tag.find_all_next(['h1', 'p']):
                    if tag.name == 'h1' and tag.get('class') == ['level1']:  # Found next section
                        break
                    if tag.name == 'h1' and tag.get('id'):  # It's a subsection
                        title_text = tag.get_text(strip=True)

                        # Find corresponding <p> tag for this subsection
                        corresponding_p_tag = soup.find('p', id=lambda x: x and x.startswith(tag.get('id', '')))
                        content_text = corresponding_p_tag.get_text(strip=True) if corresponding_p_tag else "No content"
                        
                        # Try to get the subsection URL (use Selenium to extract it)
                        subsection_url = None
                        try:
                            subsection_link_tag = tag.find_element(By.XPATH, './/preceding::a[1]')
                            if subsection_link_tag and subsection_link_tag.get_attribute('href'):
                                subsection_url = subsection_link_tag.get_attribute('href').strip()
                        except Exception as e:
                            print(f"Error extracting URL for subsection {title_text}: {e}")

                        # Add subsection data
                        section_data["subsections"].append({
                            "title": title_text,
                            "content": content_text,
                            "subsection_url": subsection_url
                        })
                        subsections_found = True

                # Only append section data if subsections were found
                if subsections_found:
                    section_data["section_url"] = section_url
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

driver.quit()  # Close the WebDriver
