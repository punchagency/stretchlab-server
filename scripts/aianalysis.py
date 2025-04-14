from openai import OpenAI
from logging_config import setup_logging
import json
import os
from util.helper import get_html_hash, load_json, save_json
import logging


# setup_logging("ai_analysis.log", logging.INFO)


# OpenAI configuration
client = OpenAI()
CACHE_FILE = "cache/ai_analysis_cache.json"
REPORT_CACHE_FILE = "cache/ai_report_analysis_cache.json"


os.makedirs("cache", exist_ok=True)


# Analysing scrapped data


def extract_data_from_html(html):
    cache = load_json(CACHE_FILE)
    html_hash = get_html_hash(html)
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
    except Exception as e:
        # Fallback if anything goes wrong
        print("openAi error", e)
        data = {
            "client_name": "",
            "member_rep_name": "",
            "flexologist_name": "",
            "key_note": "",
            "status": "",
            "booking_date": "",
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
    cache = load_json(CACHE_FILE)
    html_hash = get_html_hash(html + str(first))
    if html_hash in cache:
        print(f"Cache hit for notes HTML hash {html_hash}")
        return cache[html_hash]
    print(f"Cache miss for notes HTML hash {html_hash}, analyzing...")
    prompt = None
    if first:
        print("first_timer prompt")
        prompt = """ Concisely analyze the provided HTML, focusing only on notes or content with timestamps matching today's date. Extract and evaluate the following:
        - Note moments of progress (e.g., decisions made, actions taken, or positive updates) with their timestamps.
        - Suggest what could have been done better (e.g., missed opportunities, incomplete notes).
        - Provide an overall analysis summary for today’s notes.
        - Assign a score (0-100) based on effectiveness and clarity of today’s notes.
        - Include a rubric analysis with scores (0-10) for: Clarity, Detail, Progress, and Actionability.
        Return a JSON object with these fields: 'progress_moments', 'improvements', 'summary', 'score', 'rubric'. Use empty arrays or 'N/A' if no notes match today’s date. Here’s the HTML:

        {html}
        """
    else:
        print("not_first_timer prompt")

        prompt = """
        Concisely analyze the entire provided HTML concisely, assuming it contains notes. Extract and evaluate the following:
        - Note moments of progress (e.g., decisions made, actions taken, or positive updates) with their timestamps.
        - Suggest what could have been done better (e.g., missed opportunities, unclear communication).
        - Provide an overall analysis summary.
        - Assign a score (0-100) based on effectiveness and clarity of the conversation.
        - Include a rubric analysis with scores (0-10) for: Clarity, Engagement, Progress, and Responsiveness.
        Return a JSON object with these fields:  'progress_moments', 'improvements', 'summary', 'score', 'rubric'. Use empty arrays or 'N/A' for missing data. Here’s the HTML:

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
        cache[html_hash] = data
        save_json(CACHE_FILE, cache)
    except Exception as e:
        # Fallback if anything goes wrong
        print("openAi error", e)
        data = {
            "client_name": "",
            "member_rep_name": "",
            "flexologist_name": "",
            "key_note": "",
            "status": "",
            "booking_date": "",
        }

    return data
