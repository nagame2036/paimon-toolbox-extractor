import functools

from _data.data_json import *
from _data.i18n_json import *
from _utils.utils import *
from stat_type import *

min_weapon_rarity = 3

weapon_type_mapping = {
    'WEAPON_SWORD_ONE_HAND': 1,
    'WEAPON_CLAYMORE': 2,
    'WEAPON_POLE': 3,
    'WEAPON_CATALYST': 4,
    'WEAPON_BOW': 5,
}

weapon_curve_mapping = {
    'GROW_CURVE_ATTACK_101': 'ATK-101',
    'GROW_CURVE_ATTACK_102': 'ATK-102',
    'GROW_CURVE_ATTACK_103': 'ATK-103',
    'GROW_CURVE_ATTACK_104': 'ATK-104',
    'GROW_CURVE_ATTACK_105': 'ATK-105',
    'GROW_CURVE_CRITICAL_101': 'CHC-101',
    'GROW_CURVE_ATTACK_201': 'ATK-201',
    'GROW_CURVE_ATTACK_202': 'ATK-202',
    'GROW_CURVE_ATTACK_203': 'ATK-203',
    'GROW_CURVE_ATTACK_204': 'ATK-204',
    'GROW_CURVE_ATTACK_205': 'ATK-205',
    'GROW_CURVE_CRITICAL_201': 'CHC-201',
    'GROW_CURVE_ATTACK_301': 'ATK-301',
    'GROW_CURVE_ATTACK_302': 'ATK-302',
    'GROW_CURVE_ATTACK_303': 'ATK-303',
    'GROW_CURVE_ATTACK_304': 'ATK-304',
    'GROW_CURVE_ATTACK_305': 'ATK-305',
    'GROW_CURVE_CRITICAL_301': 'CHC-301',
}

_marked_items = {
    11304,  # 暗铁剑
}


@functools.lru_cache
def get_weapon_list() -> dict:
    items = {}
    codex = sorted((x for x in weapon_codex_config_data), key=lambda x: x['WeaponId'])
    for codex_item in codex:
        config_id = codex_item['WeaponId']
        item = _get_item(config_id)
        rarity = item['RankLevel']
        if not codex_item.get('IsDisuse') and rarity >= min_weapon_rarity:
            _put_item(items, config_id, item, rarity)
    for mark_id in _marked_items:
        _put_item(items, mark_id)
    return sort_dict(items)


@functools.lru_cache
def _get_item(config_id: int) -> dict:
    return next(x for x in weapon_config_data if x['Id'] == config_id)


def _put_item(items: dict, config_id: int, item=None, rarity=None):
    if item is None:
        item = _get_item(config_id)
    if rarity is None:
        rarity = item['RankLevel']
    items[config_id] = {
        'item': item,
        'rarity': rarity,
        'ability': _get_ability(item),
    }


def get_item_stats(item: dict) -> dict:
    return {
        stat_mapping[x['PropType']]: {
            'init': to_float(x['InitValue']),
            'curve': weapon_curve_mapping[x['Type']]
        }
        for x in item['WeaponProp']
    }


def get_item_ascensions(item: dict) -> [dict]:
    return [x for x in weapon_ascension_config_data if x['WeaponPromoteId'] == item['WeaponPromoteId']]


_ability_value_pattern = re.compile(r'<color=#\S+?>(.*?)</color>')


def _get_ability(item: dict) -> dict:
    extracted = {
        'meta': {},
        'stats': [],
        'params': [],
        'values': [],
    }
    for ability in (x for x in equipment_affix_config_data if x['Id'] in item['SkillAffix']):
        extracted['meta']['config'] = ability['OpenConfig']
        extracted['meta']['name'] = ability['NameTextMapHash']
        desc_hash = ability['DescTextMapHash']
        extracted['meta']['desc'] = desc_hash

        extracted['params'].append([to_float(x) for x in ability['ParamList'] if x != 0])
        stats = {stat_mapping[x['PropType']]: to_float(x['Value']) for x in ability['AddProps'] if x != {}}
        if stats != {}:
            extracted['stats'].append(stats)
        desc_text = lang_zhs_config[str(desc_hash)]
        extracted['values'].append(_ability_value_pattern.findall(desc_text))
    if len(extracted['stats']) == 0:
        extracted.pop('stats')
    return extracted
