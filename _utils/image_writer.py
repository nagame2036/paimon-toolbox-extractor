import os
from concurrent.futures import ThreadPoolExecutor

import requests

from _utils.data_writer import write_json
from _utils.meta import *
from _utils.utils import sort_dict

_item_images = {}


def add_image_mapping(item_type: str, items: dict, prefix: str, ext='png'):
    _item_images[item_type] = {
        'prefix': prefix,
        'ext': ext,
        'items': sort_dict(items),
    }
    print(f'mapped {item_type} image')


def write_image_json():
    write_json(f'{paimon_output}/data/image', 'image-mapping', _item_images)


def save_remote_image():
    image_data = []
    for item_type, image_info in _item_images.items():
        prefix = image_info['prefix']
        ext = image_info['ext']
        target_path = f'{view_output}/images/{item_type}'
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        for item_id, item_image in image_info['items'].items():
            image_data.append({'file': f'{target_path}/{item_id}.png', 'url': f'{prefix}{item_image}.{ext}'})
    with ThreadPoolExecutor() as executor:
        for data, response in executor.map(_save_image, image_data):
            file_name = data['file']
            with open(file_name, 'wb') as file:
                status_code = response.status_code
                if status_code == 200:
                    file.write(response.content)
                    print(f'wrote image {file_name}')
                else:
                    url = data["url"]
                    print(f'Http error {status_code} on fetch {url=}')


def _save_image(data):
    response = requests.get(data['url'])
    return data, response
