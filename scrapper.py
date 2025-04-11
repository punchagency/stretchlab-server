from scrapegraphai.graphs import SmartScraperGraph
from dotenv import load_dotenv
import os
from logging_config import setup_logging
from aianalysis import extract_data_from_html, extract_notes_and_analyse

# from database import save_booking_data
import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Logging info into the app.log, you can check logging_config.py for logging setup
setup_logging("booking_list.log", logging.INFO)

# Loading env instance
load_dotenv()

# Initilaizing variables with the env values
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
INITIAL_URL = os.getenv("INITIAL_URL")
TARGET_URL = os.getenv("TARGET_URL")


# A worker function to get the information needed for the website
def get_page_scraping(authenticate=False, url=INITIAL_URL):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.set_default_timeout(60000)
            page.goto(url)

            if authenticate:
                booking_data = []
                page.fill("input[name='uid']", USERNAME)
                page.fill("input[name='pw']", PASSWORD)
                page.click("input[type='submit']")
                page.wait_for_url(TARGET_URL)
                print(f"the new target url {page.url}")
                REDIRECT_URL = page.url
                # Wait for the select element to ensure it's loaded
                page.wait_for_selector("select[name='stores']")
                select_element = page.query_selector("select[name='stores']")
                option_elements = select_element.query_selector_all("option")
                num_options = len(option_elements)
                for i in range(num_options):
                    page.wait_for_selector("select[name='stores']")
                    select_element = page.query_selector("select[name='stores']")
                    option_elements = select_element.query_selector_all("option")

                    option = option_elements[i]
                    value = option.get_attribute("value")
                    location_name = option.inner_text()
                    print(f"Processing location: {location_name}")

                    page.select_option("select[name='stores']", value=value)
                    page.click("input[name='Submit2']")
                    page.wait_for_load_state("networkidle")

                    page.click("ul.dropdown li a:has-text('Bookings')")
                    page.wait_for_load_state("networkidle")

                    table_containing_calendar = page.query_selector(
                        ".gridContent>table"
                    )
                    if not table_containing_calendar:
                        print("Calendar table not found, skipping...")
                        continue

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
                                                open_work_it = (
                                                    modal_details.query_selector(
                                                        "[onclick*='openWorkit']"
                                                    )
                                                )
                                                if open_work_it is not None:
                                                    open_work_it.click()

                                                    work_it = page.wait_for_selector(
                                                        "#workitinner",
                                                        state="visible",
                                                    )

                                                    print("opened workit")
                                                    work_it.query_selector(
                                                        "#wktab1"
                                                    ).click()
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
                                                    information_table = (
                                                        page.query_selector(
                                                            "#workitcontactcall"
                                                        )
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
                                        page.screenshot(path="timeout_debug.png")

                                    # Take a screenshot for debugging
                                    page.screenshot(
                                        path=f"modal_debug_{location_name}.png"
                                    )

                    try:
                        # Navigate to reports(reports function)
                        page.click("ul.dropdown li a:has-text('Reports')")
                        sidebar = page.wait_for_selector("#sidebar", state="visible")
                        sidebar.query_selector(
                            "#group-12 ul li a:has-text('Booking Events Log')"
                        ).click()
                        booking_page = page.wait_for_selector(
                            "#ReportView reportDiv-0", state="visible"
                        )
                        page.wait_for_function(
                            "element => element.isConnected && element.offsetParent !== null",
                            arg=booking_page,
                        )
                        page.screenshot(path="report_page_analysis.png")

                        close_modal = page.query_selector("#userpilot-next-button")
                        if close_modal:
                            close_modal.click()
                            page.wait_for_selector("#userpilotContent", state="hidden")

                    except Exception as e:
                        page.screenshot(path="report_bug_view.png")
                        if close_modal:
                            close_modal.click()
                            page.wait_for_selector("#userpilotContent", state="hidden")

                    # Navigate back to the selection page safely
                    page.goto(REDIRECT_URL)
                    page.wait_for_selector("select[name='stores']")
                    page.screenshot(path="modal_debug_return_back.png")
                # Return the list

                return booking_data

            else:
                print("Some thing else to do if we do not need authentication")

            browser.close()
    except Exception as e:
        print(f"Critical error in scraping: {e}")
        raise


# Handle authentication and scraping authenticated content
def get_autenticated_content():
    result = get_page_scraping(True)
    print("booking result", result)
    logging.info(f"the result for booking data: {str(result)}")
    # save_booking_data(result)


get_autenticated_content()
