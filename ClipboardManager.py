import base64
import io
import os

import win32con
from PIL import ImageGrab, Image
from win32clipboard import GetClipboardData, OpenClipboard, CloseClipboard, EnumClipboardFormats


def extract_file_base64_from_list(file_paths):
    encoded_files = []

    for file_path in file_paths:
        # 'rb' specifies read bytes
        with open(file_path, 'rb') as f:
            base64_str = base64.b64encode(f.read())
            file_name = os.path.split(file_path)[1]
        _result = {"name": file_name, "content": base64_str.decode('utf-8')}
        encoded_files.append(_result)
    return encoded_files


def get_clipboard():
    OpenClipboard()
    formats = []
    last_format = 0
    while True:
        next_format = EnumClipboardFormats(last_format)
        if next_format == 0:  # this means we have enumerated all formats
            break
        else:
            formats.append(next_format)
            last_format = next_format
    try:
        if not formats:
            return None
        elif 13 in formats:
            return {'type': "text", 'data': GetClipboardData(13)}
        elif 1 in formats:
            return {'type': "text", 'data': GetClipboardData(1)}
        elif win32con.CF_BITMAP in formats:
            image = ImageGrab.grabclipboard()
            # In certain cases pictures will be copied as paths
            if isinstance(image, list):
                image = Image.open(image[0])

            image_data = io.BytesIO()
            image.save(image_data, format='PNG')
            image_data_bytes = image_data.getvalue()
            encoded_image = base64.b64encode(image_data_bytes).decode('utf-8')
            OpenClipboard()
            return {'type': "file", 'data': [{"name": "clip_image", "content": encoded_image}]}
        elif 15 in formats:
            file_list = file_paths = GetClipboardData(15)
            encoded_files = extract_file_base64_from_list(file_list)
            return {'type': "file", 'data': encoded_files}
    finally:
        CloseClipboard()
