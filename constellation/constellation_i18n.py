from _data.i18n_json import *
from _utils.i18n_writer import *
from character import *

_constellation_default = {
    1001: {
        'zh-hans': '旅人座 (风)',
        'en': 'Viator (Anemo)',
        'ja': '旅人座 (風)'
    },
    1002: {
        'zh-hans': '旅人座 (岩)',
        'en': 'Viator (Geo)',
        'ja': '旅人座 (岩)'
    },
}


def _write_constellation():
    names = {}
    profile_list = get_profile_list()
    for item in get_constellation_list().values():
        item_id = item['id']
        profile = profile_list[item_id]
        after = profile['AvatarConstellationAfterTextMapHash']
        names[item_id] = after if lang_zhs_config[str(after)] != '' else profile['AvatarConstellationBeforTextMapHash']
    write_i18n_mapping('constellation', names, defaults=_constellation_default)


def _write_constellation_level():
    names = {k: v['NameTextMapHash'] for x in get_constellation_list().values() for k, v in x['items'].items()}
    write_i18n_mapping('constellation-level', names)


def write_constellation_i18n():
    _write_constellation()
    _write_constellation_level()
