import os

def detect_file_type(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == '.sclpl':
        return 'sclpl'
    elif ext in ['.txt', '']:
        return 'text'
    else:
        return 'unknown'
