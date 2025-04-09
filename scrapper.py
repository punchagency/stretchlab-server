from scrapegraphai.graphs import SmartScraperGraph
from dotenv import load_dotenv
import os
from logging_config import setup_logging
import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Logging info into the app.log, you can check logging_config.py for logging setup
setup_logging('app.log', logging.INFO)

# Loading env instance
load_dotenv()

# Initilaizing variables with the env values
API_KEY = os.getenv("OPENAI_API_KEY")
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
INITIAL_URL = os.getenv('INITIAL_URL')
TARGET_URL = os.getenv('TARGET_URL')


# Scrapper configuration
graph_config = {
    "llm": {
        "api_key": API_KEY,
        "model": "gpt-4o",
    },
    "headless": True
}

# Function to log in, get authenticated page content and get other page contents

def get_page_scraping(authenticate=False, url=INITIAL_URL):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto(url)
        if authenticate:
            page.fill("input[name='uid']", USERNAME)
            page.fill("input[name='pw']", PASSWORD)
            page.click("input[type='submit']")
            page.wait_for_url(TARGET_URL, timeout=60000)
            print(f'the new target url {page.url}')
            REDIRECT_URL=page.url
            # Wait for the select element to ensure it's loaded
            page.wait_for_selector("select[name='stores']", timeout=10000)
            select_element = page.query_selector("select[name='stores']")
            option_elements = select_element.query_selector_all("option")
            num_options = len(option_elements)
            for i in range(num_options):
                page.wait_for_selector("select[name='stores']", timeout=20000)
                select_element = page.query_selector("select[name='stores']")
                option_elements = select_element.query_selector_all("option")
                
                option = option_elements[i]
                value = option.get_attribute("value")
                location_name = option.inner_text() 
                print(f"Processing location: {location_name}")
                
                page.select_option("select[name='stores']", value=value)
                page.click("input[name='Submit2']")
                page.wait_for_load_state("networkidle", timeout=60000)
                
                page.click("ul.dropdown li a:has-text('Bookings')")
                page.wait_for_load_state("networkidle", timeout=60000)
                
                table_containing_calendar = page.query_selector('.gridContent>table')
                if not table_containing_calendar:
                    print("Calendar table not found, skipping...")
                    continue
                
                flexologist_work_day = table_containing_calendar.query_selector_all(".cr-container-full")
                for container in flexologist_work_day:
                    children = container.query_selector_all("[onclick*='selectbooking']")
                    if len(children) > 0:
                        for child in children:
                            child.click()
                            print("Clicked booking child")
                            
                            try:
                               
                                modal_details = page.wait_for_selector(".fancybox-skin", state="visible", timeout=0)
                                if modal_details:
                                    close_btn = None
                                    modal_type = modal_details.query_selector('table[width="650"]')
                                    if modal_type:
                                        close_btn = modal_type.query_selector('[onclick*=clearall]')
                                    else:
                                        close_btn = page.wait_for_selector(".fancybox-close", state="visible", timeout=20000)
                                    # print('inner html', modal_details.inner_html())
                                    result = handle_scraping_analysis('what does this entail?. please return output in well formatted json, ensure to avoid double curly braces when returning the content; make sure the content value is text and not json. Also avoid using phrases like "The content", "The scraped data", "This entails", "The information" or any phrase that ties the content output to scraped html or sounding unsure, using phrases like "It seems" when starting the content', modal_details.inner_html())
                                    print("Scraping Result:")
                                    print(result)
                                    logging.info(f'the result for {location_name}: {str(result)}')
                                    
                                    if close_btn:
                                        close_btn.click()
                                        # print("Modal closed successfully")
                                        page.wait_for_selector(".fancybox-skin", state="hidden", timeout=10000)
                                        # print("Modal is no longer visible")
                                    else:
                                        print("Close button not found")
                                else:
                                    print("Modal not found")
                            except PlaywrightTimeoutError as e:
                                print(f"Timeout waiting for modal: {e}")
                                page.screenshot(path="timeout_debug.png")
                            
                            # Take a screenshot for debugging
                            page.screenshot(path=f"modal_debug_{location_name}.png")
                
                # Navigate back to the selection page safely
                page.goto(REDIRECT_URL)
                # print('NEW TARGET URL', REDIRECT_URL)
                page.wait_for_selector("select[name='stores']", timeout=20000)
                page.screenshot(path="modal_debug_return_back.png")
            
        browser.close()


# Handle scraping function definition
def handle_scraping_analysis(prompt, source):
    smart_scraper_graph = SmartScraperGraph(
        prompt=prompt,
        source=source,
        config=graph_config
    )

    try:
        result = smart_scraper_graph.run()
        return result
    except Exception as e:
        print(f"Error occurred: {str(e)}")

    # result = smart_scraper_graph.run()
   
    # return result



# Handle authentication and scraping authenticated content
locations=[]
def get_autenticated_content():
    get_page_scraping(True)


get_autenticated_content()




