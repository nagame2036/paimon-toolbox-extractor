from _utils.i18n_writer import *
from character import *


def _write_talent():
    names = {item_id: item['NameTextMapHash'] for item_id, item in get_talent_list()['talents'].items()}
    write_i18n_mapping('talent', names, remove_prefix={
        'zh-hans': [
            '普通攻击·',
        ],
        'en': [
            'Normal Attack: ',
        ],
        'ja': [
            '通常攻撃·',
        ],
    })


def write_talent_i18n():
    _write_talent()
