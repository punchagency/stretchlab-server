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


# Initialize table, to check if connection works
table = api.table(BASEID, TABLEID)

booking_table = api.table(BASEID, BOOKINGTABLEID)

result = table.all()


# Function for the saving of data for booking data
def save_booking_data(booking_data):
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
            "Pre-Visit Preparation(rubric)": str(
                entry["notes_analysis"]["rubric"]["pre_visit"]
            ),
            "Session Notes(rubric)": str(
                entry["notes_analysis"]["rubric"]["session_notes"]
            ),
            "Missed Sale Follow-Up(rubric)": str(
                entry["notes_analysis"]["rubric"]["missed_sale"]
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
    for location, value in unlogged_booking["results"].items():
        print(f"Processing {location}: {value}")

        if isinstance(value, list):
            print(f"  {location} has {len(value)} items in list")
            for item in value:
                fields = {
                    "Full Name": f'{item["first_name"]} {item["last_name"]}',
                    "Booking Location": item["booking_location"],
                    "Booking ID": item["booking_id"],
                    "Booking Detail": item["booking_detail"],
                    "Log Date": item["log_date"],
                    "Session Mins": item["session_mins"],
                    "Booking With": item["booking_with"],
                    "Booking Date": item["booking_date"],
                }
                # Create a new record in Airtable for booking data

                try:
                    new_record = booking_table.create(fields)
                    print(
                        f"Created record for {item["first_name"]}: {new_record['id']}"
                    )
                except Exception as e:
                    print(f"Error creating record for {item["first_name"]}: {str(e)}")
                pass
        elif isinstance(value, str):
            print(f"  {location} has status: {value}")
        else:
            print(f"  {location} has unexpected value type: {type(value)}")


print("Finished adding rows to Unlogged booking table.")
