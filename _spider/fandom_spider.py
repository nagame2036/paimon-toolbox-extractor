import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

import requests

from _data.i18n_json import lang_en_config, lang_zhs_config
from _utils.image_writer import add_image_mapping


def get_fandom_icon_urls(items: dict) -> dict:
    ret = {}
    for item_id, name_hash in items.items():
        name_en = lang_en_config[str(name_hash)]
        quoted = urllib.parse.quote(name_en.replace(' ', '_'))
        ret[item_id] = {
            'name': lang_zhs_config[str(name_hash)],
            'nameEn': name_en,
            'quoted': quoted,
            'url': f'https://genshin-impact.fandom.com/wiki/Special:Search?query={quoted}&scope=internal&contentType=&ns%5B0%5D=6#',
        }
    return ret


def write_fandom_images(item_type: str, items: dict, defaults: dict = None, file_map=lambda x: x):
    if defaults is None:
        defaults = {}
    url = 'https://static.wikia.nocookie.net/gensin-impact/images/'
    ext = 'png'
    ret = {}
    for item_id, item in defaults.items():
        ret[item_id] = item
        items.pop(item_id)
    with ThreadPoolExecutor() as executor:
        for item_id, response in executor.map(_get_response, items.items()):
            info = items[item_id]
            name = info["name"]
            name_en = info["nameEn"]
            image_info = f'{item_type=} {item_id=} {name=} {name_en=}'
            if response.status_code != 200:
                print(f'Http error {response.status_code} on fetch {image_info}')
            pattern = re.compile(f'{url}(.*?{file_map(info["quoted"])}).{ext}')
            res = pattern.findall(response.text)
            print(f'fetched fandom image: {image_info}')
            res_count = len(res)
            if res_count == 0:
                print(f'image not found: {image_info}')
            else:
                ret[item_id] = res[0]
    add_image_mapping(item_type, ret, url, ext)


def _get_response(url_pair: [int, str]):
    return url_pair[0], requests.get(url_pair[1]['url'])
