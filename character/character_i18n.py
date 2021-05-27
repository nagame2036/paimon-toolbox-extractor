from _utils.i18n_writer import *
from character.character_meta import *


def _write_character():
    names = {item_id: item['NameTextMapHash'] for item_id, item in get_character_list().items()}
    write_i18n_mapping('character', names, {
        1001: {
            'zh-hans': '空 (风)',
            'en': 'Aether (Anemo)',
            'ja': '空 (風)',
        },
        1002: {
            'zh-hans': '空 (岩)',
            'en': 'Aether (Geo)',
            'ja': '空 (岩)',
        },
        1011: {
            'zh-hans': '荧 (风)',
            'en': 'Lumine (Anemo)',
            'ja': '蛍 (風)',
        },
        1012: {
            'zh-hans': '荧 (岩)',
            'en': 'Lumine (Geo)',
            'ja': '蛍 (岩)',
        },
    })


def write_character_i18n():
    _write_character()
