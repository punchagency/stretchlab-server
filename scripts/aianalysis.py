from openai import OpenAI, RateLimitError
from logging_config import setup_logging
import json
import os
from util.helper import get_html_hash, load_json, save_json
import logging
from datetime import date
import time


# setup_logging("ai_analysis.log", logging.INFO)


# OpenAI configuration
client = OpenAI()
CACHE_FILE = "cache/ai_analysis_cache.json"
NOTE_CACHE_FILE = "cache/ai_note_analysis_cache.json"
REPORT_CACHE_FILE = "cache/ai_report_analysis_cache.json"


os.makedirs("cache", exist_ok=True)

today = str(date.today())

# Analysing scrapped data


def extract_data_from_html(html, location_name):
    cache = load_json(CACHE_FILE)

    if cache.get("last_run_date") != today:
        print(f"New day detected ({today}), clearing ai html cache")
        checkpoint = {
            "last_run_date": today,
        }
        save_json(CACHE_FILE, checkpoint)

    cache = load_json(CACHE_FILE)

    html_hash = get_html_hash(html + location_name.strip().lower())
    if html_hash in cache:
        print(f"Cache hit for modal HTML hash {html_hash}")
        return cache[html_hash]
    print(f"Cache miss for modal HTML hash {html_hash}, analyzing...")

    prompt = """
    Analyze the provided HTML concisely and extract these fields:
    - 'client_name': Text under "Name" or "Session Credit Belongs To" (exclude IDs in brackets).
    - 'member_rep_name': Not explicitly labeled; return 'N/A' if cannot get.
    - 'workout_type': Usually something like Stretch 25 Mins, check for something similar.
    - 'flexologist_name': Text under "Instructor".
    - 'key_note': Text under "Key Note".
    - 'status': Text under "Status".
    - 'booking_date': Date from "Date & Time" (before the colon).
    Return a JSON object with these exact field names, using "" for missing fields. Here’s the HTML:

    {html}
    """

    max_retries = 3
    retry_delay = 7

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You’re a data extractor that always returns JSON.",
                    },
                    {"role": "user", "content": prompt.format(html=html)},
                ],
                temperature=0,
            )
            result = response.choices[0].message.content
            if not isinstance(result, str):
                raise ValueError("Response content is not a string")

            cleaned_result = result.strip()
            if cleaned_result.startswith("```json"):
                cleaned_result = cleaned_result[7:-3].strip()

            data = json.loads(cleaned_result)
            cache[html_hash] = data
            save_json(CACHE_FILE, cache)
            print(data)
            return data

        except RateLimitError as e:
            print(f"Rate limit error: {e}")
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2**attempt)
                print(f"Retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                print("Max retries reached")
                break
        except Exception as e:
            print(f"OpenAI error: {e}")
            break
    data = {
        "client_name": "Could not process",
        "member_rep_name": "Could not process",
        "flexologist_name": "Could not process",
        "key_note": "Could not process",
        "status": "Could not process",
        "booking_date": "Could not process",
    }

    return data


def extract_unlogged_booking_from_html(html):
    # cache = load_json(REPORT_CACHE_FILE)
    # html_hash = get_html_hash(html)
    # if html_hash in cache:
    #     print(f"Cache hit for booking HTML hash {html_hash}")
    #     return cache[html_hash]
    # print(f"Cache miss for booking HTML hash {html_hash}, analyzing...")

    prompt = """
    Analyze the provided TABLE HTML concisely and extract these fields for each row:
    - 'first_name': Text under "First Name".
    - 'last_name': Text under "Last Name".
    - 'log_date': Text under "Log Date".
    - 'booking_location': Text under "Booking Location".
    - 'booking_detail': Text under "Booking Detail".
    - 'booking_id': Text under "Booking ID".
    - 'session_mins': Text under "Session Mins".
    - 'booking_with': Text under "Booking With".
    - 'booking_date': Text under "Booking Date".
    Return an Array containing JSON object with these exact field names, using N/A for missing fields. And if there is no unlogged booking return a string saying "No unlogged booking" Here’s the HTML:

    {html}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You’re a data extractor that always returns JSON.",
                },
                {"role": "user", "content": prompt.format(html=html)},
            ],
            temperature=0,
        )
        result = response.choices[0].message.content
        if not isinstance(result, str):
            raise ValueError("Response content is not a string")

        cleaned_result = result.strip()
        if cleaned_result.startswith("```json"):
            cleaned_result = cleaned_result[7:-3].strip()

        data = json.loads(cleaned_result)
        # cache[html_hash] = data
        # save_json(CACHE_FILE, cache)
    except Exception as e:
        # Fallback if anything goes wrong
        print("openAi error", e)
        data = "No Unlogged data"

    return data


def extract_notes_and_analyse(html, first):
    cache = load_json(NOTE_CACHE_FILE)
    if cache.get("last_run_date") != today:
        print(f"New day detected ({today}), clearing ai html cache")
        checkpoint = {
            "last_run_date": today,
        }
        save_json(NOTE_CACHE_FILE, checkpoint)

    cache = load_json(NOTE_CACHE_FILE)
    html_hash = get_html_hash(html + str(first))
    if html_hash in cache:
        print(f"Cache hit for notes HTML hash {html_hash}")
        return cache[html_hash]
    print(f"Cache miss for notes HTML hash {html_hash}, analyzing...")
    prompt = None
    if first:
        print("first_timer prompt")
        prompt = """
                Analyze the provided HTML, that contain notes, and extract the following in a concise manner:

                - Progress Moments: Identify key moments of progress (e.g., decisions made, actions taken, positive updates) with their timestamps.
                - Improvements: Suggest what could have been done better (e.g., missed opportunities, unclear communication).
                - Summary: Provide an overall analysis of the conversation’s effectiveness and clarity.
                - Score: Assign a score (0-100) based on the conversation’s effectiveness and clarity.
                - Rubric Analysis: Evaluate using the following metrics (score 0-10 for each):
                
                    - Pre-Visit Preparation; check if the following is present in the notes and return one score based these under pre_visit:
                        - 24-hour confirmation phone call logged?
                        - Notes logged (via phone, text, or email) informing client of:
                        - Grip sock policy (required for safety and sanitation).
                        - Early arrival (5-10 minutes for check-in).
                        - Studio location/address.
                        - Payment collection or prepayment reminder (24 hours prior).
                        - Quality Needs Analysis in key note, covering:
                        - Reason for visit and goals.
                        - Previous resolution attempts (e.g., chiropractor, physical therapy).
                        - Lifestyle (daily routine, wellness/exercise frequency, work routine).
                        - Injuries/surgeries.
                        - Wellness goal(s) and motivation (the “why”).
                    - Session Notes; check if the following is present in the notes and return one score based these under session_notes:
                        - MAPS completed (exemptions noted for non-compliance, e.g., injury/disability)?
                        - Session note template followed for each intro, including:
                        - What was done.
                        - Why it was done.
                        - Next session plan (programming/periodization).
                        - Homework.
                        - Membership recommendation.
                    - Missed Sale Follow-Up (if prospect); check if the following is present in the notes and return one score based these under missed_sale:
                        - Consistent notes recorded for next steps?
                        - Membership recommendation included?
                        - Stated objections noted?
                        - Attempts to overcome objections documented?

                Return a JSON object with the fields: `progress_moments`, `improvements`, `summary`, `score`, `rubric`. Use empty arrays (`[]`) or `"N/A"` for missing data. Here’s the HTML:

        {html}
        """

    else:
        print("not_first_timer prompt")
        prompt = """
                Analyze the provided HTML, that contain notes, and extract the following in a concise manner. Note to only extract and analyse information with today as the date:

                - Progress Moments: Identify key moments of progress (e.g., decisions made, actions taken, positive updates) with their timestamps.
                - Improvements: Suggest what could have been done better (e.g., missed opportunities, unclear communication).
                - Summary: Provide an overall analysis of the conversation’s effectiveness and clarity.
                - Score: Assign a score (0-100) based on the conversation’s effectiveness and clarity.
                - Rubric Analysis: Evaluate using the following metrics (score 0-10 for each):
                    - Session Notes; check if the following is present in the notes and return one score based these under session_notes:
                        - MAPS completed (exemptions noted for non-compliance, e.g., injury/disability)?
                        - Session note template followed for each intro, including:
                        - What was done.
                        - Why it was done.
                        - Next session plan (programming/periodization).
                        - Homework.
                        - Membership recommendation.
                    - Missed Sale Follow-Up (if prospect); check if the following is present in the notes and return one score based these under missed_sale:
                        - Consistent notes recorded for next steps?
                        - Membership recommendation included?
                        - Stated objections noted?
                        - Attempts to overcome objections documented?

                Return a JSON object with the fields: `progress_moments`, `improvements`, `summary`, `score`, `rubric`. Use empty arrays (`[]`) or `"N/A"` for missing data. Here’s the HTML:

        {html}
        """

    max_retries = 3
    retry_delay = 8

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You’re a data extractor that always returns JSON.",
                    },
                    {"role": "user", "content": prompt.format(html=html)},
                ],
                temperature=0,
            )
            result = response.choices[0].message.content
            if not isinstance(result, str):
                raise ValueError("Response content is not a string")

            cleaned_result = result.strip()
            if cleaned_result.startswith("```json"):
                cleaned_result = cleaned_result[7:-3].strip()

            data = json.loads(cleaned_result)
            cache[html_hash] = data
            save_json(NOTE_CACHE_FILE, cache)
            return data

        except RateLimitError as e:
            print(f"Rate limit error: {e}")
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2**attempt)
                print(f"Retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                print("Max retries reached")
                break
        except Exception as e:
            print(f"OpenAI error: {e}")
            break
    data = {
        "progress_moments": [
            {"timestamp": "Could not process", "description": "Could not process"}
        ],
        "improvements": ["Could not process"],
        "summary": "Could not process",
        "score": "Could not process",
        "rubric": {
            "pre_vist": "Could not process",
            "session_notes": "Could not process",
            "missed_sale": "Could not process",
        },
    }

    return data
