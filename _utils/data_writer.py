import json
import os

from _utils.meta import *


def write_json(output_path: str, file_name: str, data):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(f'{output_path}/{file_name}.json', 'w', encoding='utf-8', newline='\n') as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=2))


def write_data_json(item_type: str, file_name: str, extracted, view=None, only_data=False):
    if view is None:
        view = extracted
    new_file_name = f'{item_type}-{file_name}'
    if not only_data:
        write_json(f'{paimon_output}/data/{item_type}', new_file_name, extracted)
    write_json(f'{view_output}/data/{item_type}', new_file_name, view)
    print(f'wrote {item_type}/{new_file_name}.json')
