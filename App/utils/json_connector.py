import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')

def read_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def append_json(filename, new_record):
    data = read_json(filename)
    data.append(new_record)
    write_json(filename, data)
def load_json(filename):
    filepath = os.path.join(os.path.dirname(__file__), '..', '..', 'data', filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    filepath = os.path.join(os.path.dirname(__file__), '..', '..', 'data', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)