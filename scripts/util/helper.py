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
