from scrapegraphai.graphs import SmartScraperGraph
from dotenv import load_dotenv
import os
from logging_config import setup_logging
from aianalysis import extract_data_from_html, extract_notes_and_analyse
from util.helper import load_json, save_json
from datetime import datetime, date

# from database import save_booking_data
import logging
from playwright.sync_api import (
    sync_playwright,
    Playwright,
    TimeoutError as PlaywrightTimeoutError,
)
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

# Logging info into the app.log, you can check logging_config.py for logging setup
setup_logging("booking_list.log", logging.INFO)

# Loading env instance
load_dotenv()

# Initilaizing variables with the env values
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
INITIAL_URL = os.getenv("INITIAL_URL")
TARGET_URL = os.getenv("TARGET_URL")


os.makedirs("debug_images_test", exist_ok=True)
# This is for caching data so the script does not repeat when something fails
os.makedirs("cache_test", exist_ok=True)
CACHE_FILE = "cache_test/ai_analysis_cache.json"
CHECKPOINT_FILE = "cache_test/scraping_checkpoint.json"


# A worker function to get the information needed for the website
def process_location(location_name: str) -> list:
    checkpoint = load_json(CHECKPOINT_FILE)
    today = str(date.today())
    if location_name in checkpoint.get("completed", []):
        print(f"Skipping {location_name} - already processed")
        return checkpoint["results"].get(location_name, [])

    booking_data = []
    try:
        # Each thread gets its own browser instance
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.set_default_timeout(60000)
            page.goto(INITIAL_URL)
            page.fill("input[name='uid']", USERNAME)
            page.fill("input[name='pw']", PASSWORD)
            page.click("input[type='submit']")
            page.wait_for_url(TARGET_URL)
            print(f"Authenticated for {location_name}, URL: {page.url}")

            page.screenshot(path=f"debug_images_test/thread_debug_{location_name}.png")

            page.wait_for_selector("select[name='stores']")
            page.select_option("select[name='stores']", label=location_name)
            page.click("input[name='Submit2']")
            page.wait_for_load_state("networkidle", timeout=0)
            print(f"Processing location: {location_name}")

            # Navigate to Bookings
            page.click("ul.dropdown li a:has-text('Bookings')")
            page.wait_for_load_state("networkidle", timeout=0)

            # Find calendar table
            table_containing_calendar = page.query_selector(".gridContent>table")
            if not table_containing_calendar:
                print(f"Calendar table not found for {location_name}, skipping...")
                return booking_data

            flexologist_work_day = table_containing_calendar.query_selector_all(
                ".cr-container-full"
            )
            if len(flexologist_work_day) > 0:
                for container in flexologist_work_day:
                    children = container.query_selector_all(
                        "[onclick*='selectbooking']"
                    )
                    if len(children) > 0:
                        for child in children:
                            infoDict = {}
                            first_timer = child.query_selector(
                                "[title='first time visitor']"
                            )
                            unpaid_booking = child.query_selector(
                                "[title='This booking is unpaid']"
                            )
                            if unpaid_booking:
                                infoDict["unpaid_booking"] = "YES"
                                print("Unpaid booking")
                            if first_timer:
                                infoDict["first_timer"] = "YES"
                                print("first timer")
                            else:
                                infoDict["first_timer"] = "NO"
                                print("not a first timer")
                            child.click()
                            print("Clicked booking child")

                            try:
                                modal_details = page.wait_for_selector(
                                    ".fancybox-skin", state="visible"
                                )
                                modal_type = None
                                if modal_details:
                                    close_btn = None
                                    modal_type = modal_details.query_selector(
                                        'table[width="650"]'
                                    )
                                    if modal_type:
                                        close_btn = modal_type.query_selector(
                                            "[onclick*='clearall']"
                                        )
                                    else:
                                        close_btn = page.wait_for_selector(
                                            ".fancybox-close",
                                            state="visible",
                                        )

                                    # result = extract_data_from_html(
                                    #     modal_details.inner_html()
                                    # )
                                    infoDict["location"] = location_name
                                    # infoDict["booking_data"] = (
                                    #     result["content"]
                                    #     if "content" in result and result["content"]
                                    #     else result
                                    # )

                                    if not modal_type:
                                        print("entered workit")
                                        open_work_it = modal_details.query_selector(
                                            "[onclick*='openWorkit']"
                                        )
                                        if open_work_it is not None:
                                            open_work_it.click()

                                            work_it = page.wait_for_selector(
                                                "#workitinner",
                                                state="visible",
                                            )

                                            print("opened workit")
                                            work_it.query_selector("#wktab1").click()
                                            contact = work_it.query_selector(
                                                "#wk_contact"
                                            )
                                            print("Got to contact")
                                            page.wait_for_function(
                                                "element => element.isConnected && element.offsetParent !== null",
                                                arg=contact,
                                            )
                                            page.wait_for_function(
                                                "element => element.textContent.trim().length > 0",
                                                arg=contact,
                                            )
                                            information_table = page.query_selector(
                                                "#workitcontactcall"
                                            )
                                            close_btn = page.wait_for_selector(
                                                ".fancybox-close",
                                                state="visible",
                                            )

                                            page.wait_for_function(
                                                "element => element.isConnected && element.offsetParent !== null",
                                                arg=close_btn,
                                            )
                                            notes_tab = page.wait_for_selector(
                                                "#calltab3",
                                                state="visible",
                                            )
                                            page.wait_for_function(
                                                "element => element.isConnected && element.offsetParent !== null",
                                                arg=notes_tab,
                                            )
                                            notes_tab.click()
                                            notes = information_table.query_selector(
                                                "#callsubtab3"
                                            )
                                            print("got to notes")
                                            page.wait_for_function(
                                                "element => element.isConnected && element.offsetParent !== null",
                                                arg=notes,
                                            )
                                            page.wait_for_function(
                                                "element => element.textContent.trim().length > 0",
                                                arg=notes,
                                            )

                                            logging.info(
                                                f"here is the details for the notes {notes.inner_html()}"
                                            )

                                            # result = extract_notes_and_analyse(
                                            #     notes.inner_html(), first_timer
                                            # )
                                            # infoDict["notes_analysis"] = result

                                    booking_data.append(infoDict)
                                    # logging.info(f'the result for {location_name}: {str(result)}')

                                    if close_btn:
                                        close_btn.click()
                                        page.wait_for_selector(
                                            ".fancybox-skin",
                                            state="hidden",
                                        )
                                    else:
                                        print("Close button not found")
                                else:
                                    print("Modal not found")
                            except PlaywrightTimeoutError as e:
                                print(f"Timeout waiting for modal: {e}")
                                close_btn.click()
                                page.wait_for_selector(
                                    ".fancybox-skin",
                                    state="hidden",
                                )
                                page.screenshot(
                                    path="debug_images_test/timeout_debug.png"
                                )

                    # Take a screenshot for debugging
                    page.screenshot(
                        path=f"debug_images_test/modal_debug_{location_name}.png"
                    )

            close_modal = None
            try:
                # Navigate to reports(reports function)
                page.click("ul.dropdown li a:has-text('Reports')")
                sidebar = page.wait_for_selector("#sidebar", state="visible")
                print("got to reports")
                booking_menu = sidebar.query_selector("#group-12")
                booking_menu.click()
                print("clicked booking menu")

                booking_menu.query_selector(
                    "ul li a:has-text('Booking Events Log')"
                ).click()
                print("clicked booking page")
                booking_page = page.wait_for_selector(
                    "#ReportView #reportDiv-0", state="visible"
                )
                booking_page = page.wait_for_selector(
                    "#ReportView #reportDiv-0", state="visible"
                )
                page.wait_for_function(
                    "element => element.isConnected && element.offsetParent !== null",
                    arg=booking_page,
                )
                booking_calender = page.wait_for_selector(
                    "#reportDiv-0 #datewidget", state="visible"
                )
                page.wait_for_function(
                    "element => element.isConnected && element.offsetParent !== null",
                    arg=booking_calender,
                )
                print("got to choosing today")
                today_button = booking_calender.query_selector(
                    "[onclick*='datepreset']"
                )
                today_button.click()
                print("clicked today")

                page.wait_for_function(
                    """(element) => {
                        const initialClass = element.className;
                        return new Promise(resolve => {
                            setTimeout(() => {
                                const newClass = element.className;
                                resolve(newClass !== initialClass && newClass === 'selectboxon2');
                            }, 400);
                        });
                    }""",
                    arg=today_button,
                    timeout=40000,
                )

                print("clicked today again")
                print(booking_calender.query_selector("[onclick*='datepreset']"))
                page.wait_for_function(
                    "element => element.isConnected && element.offsetParent !== null",
                    arg=booking_calender,
                )
                page.screenshot(
                    path=f"debug_images_test/{location_name}_calendar_show.png"
                )
                print("calendar refreshed")
                page.select_option("select[id='EventType']", value="5")
                print("selected option")
                submit_btn = page.query_selector("input[name='showReport-0']")
                submit_btn.click()

                page.wait_for_selector(
                    "#reportViewer iframe", state="visible", timeout=40000
                )
                iframe_src = page.query_selector("#reportViewer iframe").get_attribute(
                    "src"
                )
                new_page = context.new_page()
                new_page.goto(iframe_src)
                report_data = new_page.wait_for_selector(
                    "#VisibleReportContentuxReportViewer_ctl13 table",
                    state="visible",
                )
                print("report data", report_data.inner_html())
                new_page.close()

                page.screenshot(
                    path=f"debug_images_test/{location_name}_booking_page_analysis.png"
                )

                print("completed booking page")
                close_modal = page.query_selector("#userpilot-next-button")
                if close_modal:
                    close_modal.click()
                    page.wait_for_selector("#userpilotContent", state="hidden")

            except Exception as e:
                page.screenshot(path="debug_images_test/report_bug_view.png")
                print(f"report error - {e}")
                if close_modal:
                    close_modal.click()
                    page.wait_for_selector("#userpilotContent", state="hidden")
            browser.close()
            return booking_data

    except Exception as e:
        print(f"Error processing location {location_name}: {e}")
        traceback.print_exc()
        if "browser" in locals():
            browser.close()
        return booking_data


def get_page_scraping(authenticate=False, url=INITIAL_URL, max_workers=2):

    try:
        checkpoint = load_json(CHECKPOINT_FILE)
        today = str(date.today())
        print(checkpoint.get("last_run_date") != today)
        if checkpoint.get("last_run_date") != today:
            print(f"New day detected ({today}), clearing checkpoint")
            checkpoint = {"last_run_date": today, "completed": [], "results": {}}
            save_json(CHECKPOINT_FILE, checkpoint)
        booking_data = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.set_default_timeout(60000)
            page.goto(url)

            redirect_url = url

            if authenticate:
                # Perform authentication
                page.fill("input[name='uid']", USERNAME)
                page.fill("input[name='pw']", PASSWORD)
                page.click("input[type='submit']")
                page.wait_for_url(TARGET_URL)
                print(f"Authenticated, new target URL: {page.url}")

                # Get all store options
                page.wait_for_selector("select[name='stores']")
                select_element = page.query_selector("select[name='stores']")
                option_elements = select_element.query_selector_all("option")
                locations = [
                    option.inner_text()
                    for option in option_elements
                    if option.get_attribute("value")
                ]
                browser.close()

                # Process locations in parallel
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    future_to_location = {
                        executor.submit(
                            process_location,
                            name,
                        ): name
                        for name in locations
                    }

                    # Collect results as they complete
                    for future in as_completed(future_to_location):
                        location_name = future_to_location[future]
                        try:
                            location_data = future.result()
                            booking_data.extend(location_data)
                            print(f"Completed processing for {location_name}")
                        except Exception as e:
                            print(f"Error in parallel task for {location_name}: {e}")
                            traceback.print_exc()

            else:
                print(
                    "No authentication required, implement alternative logic if needed"
                )

        return booking_data

    except Exception as e:
        print(f"Critical error in scraping: {e}")
        traceback.print_exc()
        raise


# Handle authentication and scraping authenticated content
def get_autenticated_content():
    result = get_page_scraping(True)
    print("booking result", result)
    logging.info(f"the result for booking data: {str(result)}")
    # save_booking_data(result)


get_autenticated_content()
