from collections import defaultdict

from _data.i18n_json import i18n_config
from _utils.data_writer import write_json
from _utils.meta import *

_i18n = defaultdict(lambda: {})
_i18n_orders = [
    'character',
    'talent',
    'constellation',
    'constellation-level',
    'weapon',
    'weapon-ability',
    'weapon-ability-desc',
    'artifact-set',
    'artifact',
    'artifact-ability-desc',
    'material',
]


def write_i18n_json():
    for lang, value in _i18n.items():
        items = sorted(value.items(), key=lambda pair: _i18n_orders.index(pair[0]))
        write_json(f'{paimon_output}/assets/i18n/data-extracted', lang, {'data': dict(items)})


def write_i18n_mapping(item_type: str, data: dict, defaults: dict = None, remove_prefix: dict = None, map_func=lambda x: x):
    if defaults is None:
        defaults = {}
    if remove_prefix is None:
        remove_prefix = {}
    for lang, lang_config in i18n_config.items():
        i18n = {k: map_func(_get_i18n(lang, lang_config, k, v, defaults, remove_prefix)) for k, v in data.items()}
        _write_i18n_json(item_type, lang, i18n)


def _get_i18n(lang: str, lang_data: dict, key: str, value: int, defaults: dict, remove_prefix: dict) -> str:
    result = defaults.get(key, {}).get(lang, lang_data.get(str(value)))
    for prefix in remove_prefix.get(lang, []):
        result = result.removeprefix(prefix)
    return result


def _write_i18n_json(item_type: str, lang: str, data: dict):
    _i18n[lang][item_type] = data
    write_json(f'{view_output}/i18n/{item_type}', lang, {'dict': {item_type: data}})
    print(f'wrote {item_type}/{lang}.json')
