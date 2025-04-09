import os
from pyairtable import Api
from dotenv import load_dotenv
from logging_config import setup_logging
import logging

# Logging info into the app.log, you can check logging_config.py for logging setup
setup_logging('database.log', logging.INFO)

# Loading env instance
load_dotenv()

ACCESS_TOKEN = os.getenv('AIRTABLE_TOKEN')
BASEID = os.getenv('AIRTABLE_BASE')
TABLEID = os.getenv('AIRTABLE_TABLE')

# Initializing api from airtable
api = Api(ACCESS_TOKEN)


# Initialize table
table = api.table(BASEID, TABLEID)

result = table.all()

print(result)


# Function for the saving of data
def save_booking_data(booking_data):
    # scrap dtata entry blueprint
    for entry in booking_data:
        fields = {
        "client Name": entry["client_name"],
        "First Timer": entry["First_timer"],
        "Member Rep Name": entry["member_rep_name"],
        "Flexologist Name": entry["flexologist_name"],
        "Analysis": entry["analysis"],
        "Rubric Analysis": entry["rubric_analysis"],
        "Status": entry["status"],
        "Booking Date": entry["booking_date"]
    }
    
    # Create a new record in Airtable
    try:
        new_record = table.create(fields)
        print(f"Created record for {entry['client_name']}: {new_record['id']}")
    except Exception as e:
        print(f"Error creating record for {entry['client_name']}: {str(e)}")

print("Finished adding rows to Airtable.")


