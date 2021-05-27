import re

import numpy as np

from _data.data_json import text_map_config_data


def to_float(num):
    text = str(np.float32(num))
    return int(float(text)) if text.endswith('.0') else float(text)


def read_text_map(text_map: dict):
    return {v: item['TextMapContentTextMapHash']
            for k, v in text_map.items() for item in text_map_config_data if item['TextMapId'] == k}


def sort_dict(data: dict, reverse=False):
    items = sorted(data.items())
    result = reversed(items) if reverse else items
    return dict(result)


def replace_color(source: str) -> str:
    colors = {
        '99FFFFFF': 'value',
    }
    pattern = re.compile(r'<color=#(\S+?)>.*?</color>')
    result = re.sub(pattern, r'{#\1}', source)
    for origin, new in colors.items():
        result = result.replace(f'#{origin}', f'{new}')
    return result
