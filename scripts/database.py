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

# Initializing api from airtable
api = Api(ACCESS_TOKEN)


# Initialize table
table = api.table(BASEID, TABLEID)

result = table.all()

print(result)

data = [
    {
        "first_timer": "NO",
        "location": "StretchLab Bellaire",
        "booking_data": {
            "client_name": "Mita Butschek",
            "member_rep_name": "N/A",
            "workout_type": "Stretch 25 Mins",
            "flexologist_name": "Rick Agustin",
            "key_note": "r shoulder tight, left hip flares up, sits a lot for work, stretches when she can, gotten worse, twice a week working out 1 weight day, 1 Cardio day, lingering feeling of tension, looking to try a massage gun, wants to see if it helps with two problem areas and goal is increase of flexibility maps due - month 3 - 3-18-25",
            "status": "Open",
            "booking_date": "Thursday, April 10, 2025",
        },
        "notes_analysis": {
            "progress_moments": [
                {
                    "timestamp": "APRIL 3rd : 8:53 PM",
                    "description": "Face To Face Contact: Session #16 completed with focus on hips, hams, shoulders. Goals: Increased mobility and decreased shoulder & hip tightness.",
                },
                {
                    "timestamp": "APRIL 3rd : 2:51 PM",
                    "description": "25min session completed.",
                },
                {
                    "timestamp": "MARCH 27th : 9:16 PM",
                    "description": "Face To Face Contact: Session #15 completed with focus on hips, quads, shoulders. Goals: Increased mobility and decreased shoulder & hip tightness.",
                },
                {
                    "timestamp": "MARCH 23rd : 8:00 AM",
                    "description": "Text Msg Sent: Outgoing single reminder sent with a positive message to share experiences.",
                },
                {
                    "timestamp": "MARCH 19th : 1:34 AM",
                    "description": "Agreement Scheduled Auto Cancellation: Cancelled per scheduled cancellation added on 3/17/2025.",
                },
                {
                    "timestamp": "FEBRUARY 25th : 5:36 PM",
                    "description": "Incoming response received: Confirmation of switching session to Rick due to Adrian's family emergency.",
                },
                {
                    "timestamp": "DECEMBER 18th 2024 : 5:59 PM",
                    "description": "Payment Profile Added: VISA x9445.",
                },
            ],
            "improvements": [
                "The notes could benefit from more detailed descriptions of the outcomes of sessions and interactions.",
                "There is a lack of follow-up on some automated messages, which could improve engagement.",
                "Some notes are repetitive, especially the automated ones, which could be consolidated for clarity.",
            ],
            "summary": "The notes reflect a series of interactions and updates related to fitness sessions, cancellations, and communications with clients. There are several instances of progress, such as completed sessions and resolved scheduling issues. However, the communication could be improved with more detailed follow-ups and less repetition in automated messages.",
            "score": 75,
            "rubric": {
                "Clarity": 7,
                "Engagement": 6,
                "Progress": 8,
                "Responsiveness": 7,
            },
        },
    },
    {
        "first_timer": "NO",
        "location": "StretchLab Bunker Hill",
        "booking_data": {
            "client_name": "Mita Butschek",
            "member_rep_name": "N/A",
            "workout_type": "Stretch 25 Mins",
            "flexologist_name": "Rick Agustin",
            "key_note": "r shoulder tight, left hip flares up, sits a lot for work, stretches when she can, gotten worse, twice a week working out 1 weight day, 1 Cardio day, lingering feeling of tension, looking to try a massage gun, wants to see if it helps with two problem areas and goal is increase of flexibility\n\nmaps due - month 3 - 3-18-25",
            "status": "Open",
            "booking_date": "Thursday, April 10, 2025",
        },
        "notes_analysis": {
            "progress_moments": [
                {
                    "timestamp": "APRIL 3rd : 8:53 PM",
                    "description": "Session #16 focused on hips, hams, shoulders with 2-3 PNFs each. Goals were increased mobility and decreased shoulder & hip tightness. Homework assigned: Hip stretch.",
                },
                {
                    "timestamp": "MARCH 27th : 9:16 PM",
                    "description": "Session #15 focused on hips, quads, shoulders with 2-3 PNFs each. Goals were increased mobility and decreased shoulder & hip tightness. Homework assigned: Hip stretch.",
                },
                {
                    "timestamp": "MARCH 20th : 1:28 PM",
                    "description": "Active phase with focus on lower body and shoulders to ease tension on the right shoulder blade.",
                },
                {
                    "timestamp": "FEBRUARY 14th : 10:49 AM",
                    "description": "Active phase with focus on upper body and right shoulder blade due to tightness from sitting.",
                },
            ],
            "improvements": [
                "The notes could benefit from more detailed outcomes or follow-up actions to track progress over time.",
                "There is a lack of clarity on whether the assigned homework was completed or effective.",
                "Communication could be improved by specifying any changes in the client's condition or feedback from the client.",
            ],
            "summary": "The notes document a series of fitness sessions focusing on mobility and tension relief, particularly in the shoulders and hips. Progress is noted through session details and assigned homework, but there is a lack of follow-up on the effectiveness of these actions. The communication is clear but could be enhanced with more detailed outcomes and client feedback.",
            "score": 75,
            "rubric": {
                "Clarity": 8,
                "Engagement": 7,
                "Progress": 7,
                "Responsiveness": 6,
            },
        },
    },
    {
        "first_timer": "NO",
        "location": "StretchLab Heights",
        "booking_data": {
            "client_name": "Courtney Schumann",
            "member_rep_name": "N/A",
            "workout_type": "Stretch 50 Mins",
            "flexologist_name": "Diego Lugo",
            "key_note": "Hips.......sit. MAPS Testing - 1 month  DUE 10/22",
            "status": "Open",
            "booking_date": "Thursday, April 10, 2025",
        },
        "notes_analysis": {
            "progress_moments": [
                {
                    "timestamp": "APRIL 9th : 10:07 AM",
                    "description": "Incoming response received from Courtney Schumann.",
                },
                {
                    "timestamp": "APRIL 9th : 9:55 AM",
                    "description": "Text message sent by Amy Rogers confirming a session.",
                },
                {
                    "timestamp": "APRIL 5th : 1:06 PM",
                    "description": "Client wants to adjust shoulder stretches due to pain.",
                },
                {
                    "timestamp": "APRIL 5th : 9:59 AM",
                    "description": "Booking status changed to completed.",
                },
                {
                    "timestamp": "MARCH 28th : 10:58 AM",
                    "description": "Booking status changed to completed.",
                },
                {
                    "timestamp": "FEBRUARY 27th : 9:53 AM",
                    "description": "Booking status changed to completed.",
                },
                {
                    "timestamp": "FEBRUARY 22nd : 11:12 AM",
                    "description": "Fitness note added by Guillermo Gomez.",
                },
                {
                    "timestamp": "JANUARY 30th : 9:09 AM",
                    "description": "Incoming response received from Courtney Schumann.",
                },
                {
                    "timestamp": "JANUARY 28th : 2:48 PM",
                    "description": "Text message sent by Sherri Ashworth.",
                },
                {
                    "timestamp": "OCTOBER 17th : 10:11 AM",
                    "description": "Phone call made by Sherri Ashworth, voicemail left.",
                },
                {
                    "timestamp": "OCTOBER 17th : 10:10 AM",
                    "description": "Email sent by Sherri Ashworth explaining booking issues.",
                },
            ],
            "improvements": [
                "Communication could be clearer regarding booking and cancellation policies to avoid confusion.",
                "More proactive follow-ups could be implemented to ensure client satisfaction and address any issues promptly.",
                "Automated messages should be personalized to enhance engagement.",
            ],
            "summary": "The notes reflect a series of interactions primarily focused on booking confirmations, cancellations, and client communications. There are several instances of effective communication, such as confirmations and responses to client inquiries. However, there are also areas where communication could be improved, particularly in clarifying policies and ensuring client satisfaction.",
            "score": 75,
            "rubric": {
                "Clarity": 7,
                "Engagement": 6,
                "Progress": 8,
                "Responsiveness": 7,
            },
        },
    },
    {
        "first_timer": "NO",
        "location": "StretchLab River Oaks",
        "booking_data": {
            "client_name": "Ji Rim",
            "member_rep_name": "N/A",
            "workout_type": "Stretch 25 Mins",
            "flexologist_name": "Beverly Keil",
            "key_note": "Works in oil and gas. She is swimming and walking. Her hips and general body are very sore and tight. Wants to work on helping her body recover from life. Daughter goes to a theater class on Saturday at 11:30 so that is the best time for her. MAPS Testing - 1 month",
            "status": "Session Logged As Completed 4/10/2025 6:50 AM by Ji Rim",
            "booking_date": "Thursday, April 10, 2025",
        },
        "notes_analysis": {
            "progress_moments": [
                {
                    "timestamp": "APRIL 10th : 8:01 AM",
                    "description": "Face To Face Contact: Ji and her family returned from Disney World. She had a full body stretch and responded well to all stretches. No new homework assigned.",
                },
                {
                    "timestamp": "MARCH 27th : 7:58 AM",
                    "description": "Ji came in feeling tired. Full body stretch was performed, and she responded well. Homework was assigned for quad, hip flexor, and shoulder.",
                },
                {
                    "timestamp": "MARCH 20th : 8:52 AM",
                    "description": "Ji came in feeling good. Full body stretch was performed, and she responded well. Continued focus on full body and previous homework.",
                },
                {
                    "timestamp": "MARCH 13th : 8:17 AM",
                    "description": "Face To Face Contact: Updated and reviewed MAPS. Full body stretch was performed, and right side was found tighter. Homework was assigned for calves, ITB, and hip stretches.",
                },
                {
                    "timestamp": "FEBRUARY 27th : 7:02 PM",
                    "description": "Full body stretch was performed as Ji was feeling stress and tired from work.",
                },
                {
                    "timestamp": "FEBRUARY 13th : 6:59 PM",
                    "description": "Full body stretch with focus on hips and lower back.",
                },
                {
                    "timestamp": "NOVEMBER 30th 2024 : 12:38 PM",
                    "description": "Foundation session with focus on low back and posterior chain. Felt good after session.",
                },
                {
                    "timestamp": "SEPTEMBER 22nd 2024 : 8:28 PM",
                    "description": "Intro session: Ji was curious about Stretchlab. Recommended full body stretches with focus on glutes, hamstrings, and UT.",
                },
            ],
            "improvements": [
                "Some notes are repetitive, indicating a lack of new information or progress.",
                "Communication could be clearer regarding the specific outcomes of each session.",
                "More detailed follow-up on assigned homework could enhance progress tracking.",
            ],
            "summary": "The notes document a series of fitness sessions focusing on full body stretches, with particular attention to areas of tightness such as hips, shoulders, and lower back. Progress is noted in terms of client response to stretches and assigned homework. However, there is room for improvement in communication clarity and progress tracking.",
            "score": 75,
            "rubric": {
                "Clarity": 7,
                "Engagement": 8,
                "Progress": 6,
                "Responsiveness": 7,
            },
        },
    },
]


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


print("Finished adding rows to Airtable.")


save_booking_data(data)
