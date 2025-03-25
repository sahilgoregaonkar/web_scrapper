import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Function to fetch the URL from the 'copy link' button using CDP and Selenium
def fetch_copy_link_via_cdp(url):
    try:
        # Setup WebDriver (using Chrome in this case)
        options = Options()
        options.add_argument("--headless")  # Optional: run in headless mode (no browser window)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Enable the network domain to capture network events
        driver.execute_cdp_cmd('Network.enable', {})

        # Listens for network requests and captures the response from the wa/ folder
        def handle_request(request):
            # Filter the requests that are part of the 'wa/' folder
            if 'wa/' in request['response']['url']:
                # Extract the URL from the payload or response
                return request['response']['url']

        # Register the handler for network response events
        driver.request_interceptor = handle_request

        # Open the URL
        driver.get(url)

        # Wait for the page to load and the "copy link" button to trigger the network request
        time.sleep(5)  # You can adjust this based on the page's loading time

        # Find the "copy link" button (assuming it's an anchor <a> tag with a specific class 'copy-link')
        copy_link_button = driver.find_element(By.CSS_SELECTOR, "a.copy-link")  # Adjust selector if needed
        copy_link_button.click()  # Click the button to trigger the network request

        # Wait for the network request to be captured
        time.sleep(5)  # Adjust this as needed to ensure the request has been captured

        # Close the driver
        driver.quit()

        # If we successfully captured the URL, return it
        return handle_request

    except Exception as e:
        print(f"Error fetching URL from network request: {str(e)}")
        return None

# Function to update the JSON data with the copied URL
def update_json_with_links(json_data):
    for chapter in json_data:  # Looping through the list of chapters
        if chapter.get("chapter_url") is None:
            # Fetch URL for the chapter if it's missing
            chapter_url = fetch_copy_link_via_cdp(chapter.get("section", ""))  # Adjust if needed for chapter-specific URLs
            if chapter_url:
                chapter["chapter_url"] = chapter_url

        # Loop through sections of the chapter
        for section in chapter.get("sections", []):
            if section.get("section_url") is None:
                # Fetch URL for the section if it's missing
                section_url = fetch_copy_link_via_cdp(section.get("title"))  # Adjust if needed for section-specific URLs
                if section_url:
                    section["section_url"] = section_url

            # Loop through subsections of the section
            for subsection in section.get("subsections", []):
                if subsection.get("subsection_url") is None:
                    # Fetch URL for the subsection if it's missing
                    subsection_url = fetch_copy_link_via_cdp(subsection.get("title"))  # Adjust if needed for subsection-specific URLs
                    if subsection_url:
                        subsection["subsection_url"] = subsection_url
    return json_data

# Function to save the updated JSON to the same file
def save_updated_json(json_data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    print(f"Updated JSON saved to {file_path}")

# Main function to load, process, and save the JSON data
def process_json_file(input_file_path):
    # Open and load the JSON data from the provided file path
    with open(input_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Update the JSON data with the copied URLs
    updated_json = update_json_with_links(json_data)

    # Save the updated JSON back to the same file
    save_updated_json(updated_json, input_file_path)

# Example usage
input_json_path = r'C:\Users\Admin\Desktop\web-scrapper\output.json'  # Update this with your JSON file path

# Run the process (it will modify the original file in place)
process_json_file(input_json_path)
