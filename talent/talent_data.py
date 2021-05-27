from _data.i18n_json import *
from _utils.data_writer import *
from character import *
from material import *
from talent.talent_meta import *

item_type = 'talent'


def _debug_item_list():
    item_list = get_talent_list()['talents']
    for item_id, item in item_list.items():
        name = lang_zhs_config[str(item['NameTextMapHash'])]
        if 'ProudSkillId' in item:
            print(item_id, name, item)


def _write_item_list():
    extracted_paimon = {}
    extracted_view = {}
    for item_id, item in get_talent_list()['talents'].items():
        extracted = _extract_talent(item)
        extracted_paimon[item_id] = extracted
        game_id = item.get('Id', item.get('ProudSkillGroupId'))
        extracted_view[item_id] = {'gameId': game_id} | extracted
    write_data_json(item_type, 'list', extracted_paimon, extracted_view)


def _extract_talent(item: dict) -> dict:
    if 'CostStamina' in item:
        return _extract_alternative_sprint(item)
    elif 'ProudSkillId' in item:
        return _extract_passive_talent(item)
    else:
        return _extract_combat_talent(item)


def _extract_alternative_sprint(_: dict) -> dict:
    return {}


def _extract_passive_talent(_: dict) -> dict:
    return {}


def _extract_combat_talent(item: dict) -> dict:
    materials = {
        'domain': []
    }
    group_id = 'ProudSkillGroupId'
    levels = (x for x in talent_data_config_data if x[group_id] == item[group_id])
    for level_config in levels:
        cost = [material_mapping.get(x.get('Id')) for x in level_config['CostItems']]
        if not cost[0]:
            continue
        materials['domain'].append(get_material_group_last(cost[0]))
        materials['mob'] = get_material_group_last(cost[1])
        materials['boss'] = get_material_group_last(cost[2])
        materials['event'] = get_material_group_last(cost[3])
    materials['domain'] = list(set(materials['domain']))
    return {
        'materials': materials,
    }


def _write_levelup_cost():
    extracted_paimon = []
    for item in talent_data_config_data:
        level = item.get('Level', -1)
        if level in [-1, 1] or level > max_levelup_target:
            continue
        cost = get_cost_items(item['CostItems'])
        extracted = {
            'mora': item['CoinCost'],
            'domain': get_cost_detail(cost[0]),
            'mob': get_cost_detail(cost[1]),
            'boss': cost[2]['count'],
            'event': cost[3]['count'],
        }
        extracted = {k: v for k, v in extracted.items() if v != 0}

        index = level - 2
        if len(extracted_paimon) <= index:
            extracted_paimon.append(extracted)
        elif extracted != extracted_paimon[index]:
            print(f'conflict talent levelup cost on {item["ProudSkillId"]} Lv. {level}: {extracted}')
    write_data_json(item_type, 'levelup-cost', extracted_paimon)


def write_talent_data():
    _write_item_list()
    _write_levelup_cost()


if __name__ == '__main__':
    # _debug_item_list()
    write_talent_data()
