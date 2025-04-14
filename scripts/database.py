import os
from pyairtable import Api
from dotenv import load_dotenv
from logging_config import setup_logging
import logging

# Logging info into the app.log, you can check logging_config.py for logging setup
setup_logging("database.log", logging.INFO)

# Loading env instance
load_dotenv()

ACCESS_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASEID = os.getenv("AIRTABLE_BASE")
TABLEID = os.getenv("AIRTABLE_TABLE")
BOOKINGTABLEID = os.getenv("BOOKING_TABLE_ID")
# Initializing api from airtable
api = Api(ACCESS_TOKEN)


# Initialize table, would correct to initialize diffrent tables
table = api.table(BASEID, TABLEID)

booking_table = api.table(BASEID, BOOKINGTABLEID)

result = table.all()


# Function for the saving of data
def save_booking_data(booking_data):
    # scrap dtata entry blueprint
    for entry in booking_data:
        progressive_moments = "\n\n".join(
            f"{moment['timestamp']} - {moment['description']}"
            for moment in entry["notes_analysis"]["progress_moments"]
        )
        improvements = "\n\n".join(
            f"{moment}" for moment in entry["notes_analysis"]["improvements"]
        )
        fields = {
            "Client Name": entry["booking_data"]["client_name"],
            "First Timer": entry["first_timer"],
            "Member Rep Name": entry["booking_data"]["member_rep_name"],
            "Flexologist Name": entry["booking_data"]["flexologist_name"],
            "Workout Type": entry["booking_data"]["workout_type"],
            "Location": entry["location"],
            "Key Note": entry["booking_data"]["key_note"],
            "Status": entry["booking_data"]["status"],
            "Booking Date": entry["booking_data"]["booking_date"],
            "Note Analysis(progressive moments)": progressive_moments,
            "Note Analysis(improvements)": improvements,
            "Note Summary": entry["notes_analysis"]["summary"],
            "Note Score": str(entry["notes_analysis"]["score"]),
            "Engagement(rubric)": str(entry["notes_analysis"]["rubric"]["Engagement"]),
            "Clarity(rubric)": str(entry["notes_analysis"]["rubric"]["Clarity"]),
            "Progress(rubric)": str(entry["notes_analysis"]["rubric"]["Progress"]),
            "Responsiveness(rubric)": str(
                entry["notes_analysis"]["rubric"]["Responsiveness"]
            ),
        }
        # Create a new record in Airtable

        try:
            new_record = table.create(fields)
            print(
                f"Created record for {entry["booking_data"]['client_name']}: {new_record['id']}"
            )
        except Exception as e:
            print(
                f"Error creating record for {entry["booking_data"]['client_name']}: {str(e)}"
            )


def save_unlogged_booking_data(unlogged_booking):
    # scrap dtata entry blueprint
    for entry in unlogged_booking:

        fields = {
            "Full Name": "",
            "Booking Location": "",
            "Booking ID": "",
            "Booking Detail": "",
            "Log Date": "",
            "Session Mins": "",
            "Booking With": "",
            "Booking Date": "",
        }
        # Create a new record in Airtable

        try:
            new_record = booking_table.create(fields)
            print(f"Created record for {entry[""]}: {new_record['id']}")
        except Exception as e:
            print(f"Error creating record for {entry[""]}: {str(e)}")


print("Finished adding rows to Unlogged booking table.")
