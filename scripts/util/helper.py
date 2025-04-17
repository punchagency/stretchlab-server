import os
import json
import hashlib


def load_json(file_path, default={}):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return default


def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def get_html_hash(html):
    return hashlib.md5(html.encode()).hexdigest()


def get_combined_html(tr_elements):
    combined_html = "<table>"
    for tr in tr_elements:
        try:
            html = tr.inner_html()
            combined_html += html
        except Exception as e:
            print(f"Error getting HTML for <tr>: {e}")
    combined_html += "</table>"
    return combined_html


def process_notes(notes_info):
    try:
        table = notes_info.query_selector("#addNote + table")
        if not table:
            print("No table found after #addNote")
            return ""
        tr_elements = table.query_selector_all("tr")[:7]
        if not tr_elements:
            print("No <tr> elements found in the table")
            return ""
        return get_combined_html(tr_elements)
    except Exception as e:
        print(f"Error processing table: {e}")
        return ""


def remove_duplicates_by_key_keep_last_ordered(lst, key):
    if not lst or not key:
        return []

    seen = set()
    result = []

    for item in reversed(lst):
        if not isinstance(item, dict) or "booking_data" not in item:
            continue
        try:
            key_value = item["booking_data"].get(key)
            if key_value is None:
                continue
            if key_value == "unavailable":
                result.append(item)
            elif key_value not in seen:
                seen.add(key_value)
                result.append(item)
        except (KeyError, TypeError):
            continue

    return result[::-1]
