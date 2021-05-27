from _data.i18n_json import *
from _utils.data_writer import *
from character import *

item_type = 'constellation'


def _debug_item_list():
    for info in get_constellation_list().values():
        group_id = info['id']
        for item_id, item in info['items'].items():
            name = lang_zhs_config[str(item['NameTextMapHash'])]
            print(group_id, item_id, name)


def _write_item_group():
    extracted_paimon = {info['id']: [x for x in info['items'].keys()] for info in get_constellation_list().values()}
    write_data_json(item_type, 'group', extracted_paimon)


def write_constellation_data():
    _write_item_group()


if __name__ == '__main__':
    _debug_item_list()
