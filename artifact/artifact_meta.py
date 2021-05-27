import functools

from _data.data_json import *
from _utils.utils import *
from stat_type import *

min_artifact_rarity = 4

artifact_type_mapping = {
    'EQUIP_BRACER': 1,  # 生之花
    'EQUIP_NECKLACE': 2,  # 死之羽
    'EQUIP_SHOES': 3,  # 时之沙
    'EQUIP_RING': 4,  # 空之杯
    'EQUIP_DRESS': 5,  # 理之冠
}


@functools.lru_cache
def get_artifact_set_list():
    set_list = {}
    codex = sorted((x for x in artifact_codex_config_data), key=lambda x: x['SortOrder'])
    for codex_item in codex:
        rarity = codex_item['Level']
        if rarity < min_artifact_rarity:
            continue
        set_id = codex_item['SuitId']
        set_item = _get_set_item(set_id)
        rarities = set_list.get(set_id, {'rarities': set()})['rarities']
        rarities.add(rarity)
        items = {
            1: _get_item(codex_item.get('FlowerId')),
            2: _get_item(codex_item.get('LeatherId')),
            3: _get_item(codex_item.get('SandId')),
            4: _get_item(codex_item.get('CupId')),
            5: _get_item(codex_item.get('CapId')),
        }
        items = {k: v for k, v in items.items() if v != {}}
        set_list[set_id] = {
            'rarities': rarities,
            'types': list(items.keys()),
            'set': set_item,
            'items': items,
            'abilities': _get_set_abilities(set_item),
        }
    return sort_dict(set_list)


@functools.lru_cache
def _get_set_item(config_id: int) -> dict:
    return next(x for x in artifact_set_config_data if x['SetId'] == config_id)


@functools.lru_cache
def get_artifact_list() -> dict:
    items = {}
    for set_id, set_info in get_artifact_set_list().items():
        for item_type, item in set_info['items'].items():
            item_id = f'{set_id}.{item_type}'
            items[item_id] = item
    return sort_dict(items)


@functools.lru_cache
def _get_item(config_id: int) -> dict:
    return next((x for x in artifact_config_data if x['Id'] == config_id), {})


def _get_set_abilities(set_item: dict) -> list:
    abilities = []
    for index, item in enumerate(x for x in equipment_affix_config_data if x['Id'] == set_item['EquipAffixId']):
        extracted = {
            'meta': {
                'config': item['OpenConfig'],
                'name': item['NameTextMapHash'],
                'desc': item['DescTextMapHash'],
            },
            'require': set_item['SetNeedNum'][index],
        }
        addons = {
            'stats': {stat_mapping[x['PropType']]: to_float(x['Value']) for x in item['AddProps'] if x != {}},
            'params': [to_float(x) for x in item['ParamList'] if x != 0],
        }
        for k, v in addons.items():
            if len(v):
                extracted[k] = v
        abilities.append(extracted)
    return abilities
