from openai import OpenAI
from logging_config import setup_logging
import json
import logging


setup_logging("ai_analysis.log", logging.INFO)


# OpenAI configuration
client = OpenAI()


# Analysing scrapped data


def extract_data_from_html(html):

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


def extract_notes_and_analyse(html, first):
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
