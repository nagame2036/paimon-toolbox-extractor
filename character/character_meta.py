import functools
from collections import defaultdict

from _data.data_json import *
from _utils.utils import *
from element import *
from stat_type import *

rarity_mapping = {
    'QUALITY_PURPLE': 4,
    'QUALITY_ORANGE': 5,
}

region_mapping = {
    'ASSOC_TYPE_MONDSTADT': 1,
    'ASSOC_TYPE_LIYUE': 2,
    'ASSOC_TYPE_FATUI': 7,
}

character_curve_level_mapping = {
    'GROW_CURVE_HP_S4': 'HP-S4',
    'GROW_CURVE_HP_S5': 'HP-S5',
    'GROW_CURVE_ATTACK_S4': 'ATK-S4',
    'GROW_CURVE_ATTACK_S5': 'ATK-S5',
}


@functools.lru_cache
def get_character_list() -> dict:
    return _get_heroes() | _get_others()


@functools.lru_cache
def _get_item(config_id: int) -> dict:
    return next(x for x in character_config_data if x['Id'] == config_id)


@functools.lru_cache
def _get_heroes() -> dict:
    items = {}
    codex = sorted((x for x in hero_config_data), key=lambda x: x['AvatarId'])
    counter = 0
    for config_id in (x['AvatarId'] for x in codex):
        item = _get_item(config_id)
        for talent in _get_skills(item):
            element_burst_id = talent.get('EnergySkill')
            if not element_burst_id:
                continue
            element_burst = _get_talent(element_burst_id)
            if element_burst['AbilityName'] != '':
                element = element_mapping[element_burst['CostElemType']]
                item_id = 1000 + counter * 10 + element
                items[item_id] = item
        counter += 1
    return items


@functools.lru_cache
def _get_others() -> dict:
    items = {}
    codex = sorted((x for x in character_codex_config_data), key=lambda x: x['SortFactor'])
    counter = defaultdict(lambda: 0)
    for config_id in (x['AvatarId'] for x in codex):
        item = _get_item(config_id)
        rarity = rarity_mapping[item['QualityType']]
        counter[rarity] += 1
        item_id = rarity * 1000 + counter[rarity]
        items[item_id] = item
    return sort_dict(items)


@functools.lru_cache
def get_profile_list() -> dict:
    items = {}
    for item_id, item in get_character_list().items():
        profile = next(x for x in character_profile_config_data if x['AvatarId'] == item['Id'])
        items[item_id] = profile
    return sort_dict(items)


@functools.lru_cache
def _get_skill_list() -> dict:
    items = {}
    for item_id, item in get_character_list().items():
        for skill_config in _get_skills(item):
            element_burst_id = skill_config.get('EnergySkill')
            if not element_burst_id:
                continue
            element_burst = _get_talent(element_burst_id)
            talent_element = element_mapping[element_burst['CostElemType']]
            if item_id > 4000 or item_id % 10 == talent_element:
                items[item_id] = {'element': talent_element, 'config': skill_config}
    return sort_dict(items)


def _get_skills(item: dict):
    return (x for x in character_talent_config_data if x['Id'] in {item['SkillDepotId'], *item['CandSkillDepotIds']})


_item_talents = {}
_talent_list = {}
_talent_ids = {}


@functools.lru_cache
def get_talent_list():
    for item_id, skill_data in _get_skill_list().items():
        skill_config = skill_data['config']
        element_burst_id = skill_config.get('EnergySkill')
        skills = [x for x in skill_config['Skills'] if x != 0]
        inherent = [x['ProudSkillGroupId'] for x in skill_config['InherentProudSkillOpens'] if x != {}]
        _item_talents[item_id] = {
            'element': skill_data['element'],
            'talents': [
                *_put_talent(item_id, 1, skills[:1]),  # 普攻
                *_put_talent(item_id, 2, skills[1:2]),  # 元素战技
                *_put_talent(item_id, 3, skills[2:]),  # 战斗天赋
                *_put_talent(item_id, 4, [element_burst_id]),  # 元素爆发
                *_put_talent(item_id, 5, inherent),  # 固有天赋
            ]}
    return {'items': sort_dict(_item_talents), 'talents': sort_dict(_talent_list)}


@functools.lru_cache
def _get_talent(config_id: int) -> dict:
    talent = next((x for x in talent_config_data if x['Id'] == config_id), {})
    return talent if talent != {} \
        else next(x for x in talent_data_config_data if x.get('ProudSkillGroupId') == config_id)


def _put_talent(item_id: int, talent_type: int, talent_ids: [int]) -> [int]:
    talent_results = []
    for talent_index, talent_id in enumerate(talent_ids):
        if talent_id in _talent_ids:
            talent_results.append(_talent_ids[talent_id])
        else:
            new_talent_id = item_id * 100 + talent_index * 10 + talent_type
            talent_results.append(new_talent_id)
            talent_config = _get_talent(talent_id)
            _talent_list[new_talent_id] = talent_config
            _talent_ids[talent_id] = new_talent_id
    return talent_results


_constellation_ids = {}


@functools.lru_cache
def get_constellation_list() -> dict:
    items = {}
    for item_id, skill_data in _get_skill_list().items():
        skill_config = skill_data['config']
        constellations = skill_config['Talents']
        group_id = _constellation_ids.setdefault(constellations[0], item_id)
        items[item_id] = {
            'id': group_id,
            'items': dict(_get_constellation(group_id, x) for x in constellations),
        }
    return sort_dict(items)


@functools.lru_cache
def _get_constellation(group_id: int, config_id: int):
    new_id = group_id * 10 + config_id % 10
    item = next(x for x in constellation_config_data if x['TalentId'] == config_id)
    return new_id, item


def get_curve_level(item: dict, stat_name: str, stat_type: str) -> dict:
    return {
        'init': to_float(item[stat_name]),
        'curve': [
            character_curve_level_mapping[x['GrowCurve']]
            for x in item['PropGrowCurves'] if stat_mapping[x['Type']] == stat_type
        ][0],
    }
