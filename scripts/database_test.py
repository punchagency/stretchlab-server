import random
from datetime import datetime, timedelta
import uuid


def generate_bookings():
    first_names = [
        "John",
        "Emma",
        "Michael",
        "Sarah",
        "David",
        "Lisa",
        "James",
        "Olivia",
        "Chris",
        "Sophia",
    ]
    last_names = [
        "Smith",
        "Johnson",
        "Brown",
        "Taylor",
        "Wilson",
        "Davis",
        "Clark",
        "Harris",
        "Lewis",
        "Walker",
    ]
    locations = [
        "StretchLab Bunker Hill",
        "StretchLab Pearland",
        "StretchLab Heights",
        "StretchLab River Oaks",
    ]
    instructors = ["Alex Reed", "Jamie Cole", "Morgan Lee", "Taylor Quinn", "Sam Patel"]
    session_mins = ["25", "50"]
    booking_details = [
        "Initial consultation and stretch",
        "Follow-up mobility session",
        "Recovery-focused stretch",
        "Post-workout stretch",
        "Needs analysis and goal setting",
    ]

    def random_date(start_date, end_date):
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)

    bookings = []
    for _ in range(200):
        item = {
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
            "booking_location": random.choice(locations),
            "booking_id": str(uuid.uuid4())[:8],
            "booking_detail": random.choice(booking_details),
            "log_date": random_date(start_date, end_date),
            "session_mins": random.choice(session_mins),
            "booking_with": random.choice(instructors),
            "booking_date": random_date(start_date, end_date),
        }
        bookings.append(item)
    return {"results": {"location": bookings}}
