from collections import defaultdict

from _utils.data_writer import *
from material import *
from weapon.weapon_meta import *

_output = 'weapon'


def _debug_item_list():
    for item_id, item in get_weapon_list().items():
        item_name = lang_zhs_config[str(item['NameTextMapHash'])]
        print(item_id, item_name, item)


def _write_item_list():
    extracted_paimon = {}
    extracted_view = {}
    for item_id, info in get_weapon_list().items():
        item = info['item']

        ascensions = get_item_ascensions(item)
        cost = [material_mapping.get(x.get('Id')) for x in ascensions[-1]['CostItems']]

        extracted = {
            'type': weapon_type_mapping[item['WeaponType']],
            'rarity': info['rarity'],
            'materials': {
                'domain': get_material_group_last(cost[0]),
                'elite': get_material_group_last(cost[1]),
                'mob': get_material_group_last(cost[2]),
            },
            'stats': get_item_stats(item),
            'ability': {k: v for k, v in info['ability'].items() if k != 'meta'},
        }
        extracted_paimon[item_id] = extracted
        extracted_view[item_id] = {'gameId': item['Id']} | extracted
    write_data_json(_output, 'list', extracted_paimon, extracted_view)


def _write_enhance_cost():
    extracted = {
        3: [],
        4: [],
        5: [],
    }
    for item in weapon_enhance_cost_config_data:
        for rarity, exps in extracted.items():
            exps.append(item['RequiredExps'][rarity - 1])
    write_data_json(_output, 'enhance-cost', extracted)


def _write_ascend_cost():
    extract_paimon = defaultdict(lambda: [])
    for item_id, info in get_weapon_list().items():
        for ascension in get_item_ascensions(info['item']):
            phase = ascension.get('PromoteLevel')
            if not phase:
                continue
            cost = get_cost_items(ascension['CostItems'])
            extracted = {
                'mora': ascension['CoinCost'],
                'domain': get_cost_detail(cost[0]),
                'elite': get_cost_detail(cost[1]),
                'mob': get_cost_detail(cost[2]),
            }
            rarity = info['rarity']
            if len(extract_paimon[rarity]) < 6:
                extract_paimon[rarity].append(extracted)
            elif extract_paimon[rarity][phase - 1] != extracted:
                print(f'conflict ascend cost on {item_id} ascension {phase}: {extracted}')
    write_data_json(_output, 'ascend-cost', extract_paimon)


def _write_stat_curve_level():
    extracted_paimon = defaultdict(lambda: [])
    for item in weapon_grow_curve_config_data:
        for curve in item['CurveInfos']:
            curve_type = weapon_curve_mapping.get(curve['Type'])
            if not curve_type:
                continue
            extracted_paimon[curve_type].append(to_float(curve['Value']))
    write_data_json(_output, 'stat-curve-level', extracted_paimon)


def _write_stat_curve_ascension():
    extracted_paimon = defaultdict(lambda: defaultdict(lambda: [0]))
    for item_id, info in get_weapon_list().items():
        for ascension in get_item_ascensions(info['item']):
            item_id = ascension['WeaponPromoteId']
            phase = ascension.get('PromoteLevel')
            if not phase:
                continue
            for stat in (x for x in ascension['AddProps'] if 'Value' in x):
                stat_type = stat_mapping[stat['PropType']]
                stat_value = to_float(stat['Value'])
                rarity = info['rarity']
                results = extracted_paimon[rarity][stat_type]
                if len(results) < 7:
                    results.append(stat_value)
                elif results[phase] != stat_value:
                    print(f'conflict stat {stat_type} of weapon {item_id} ascension {phase}: {stat_value}')
    write_data_json(_output, 'stat-curve-ascension', extracted_paimon)


def write_weapon_data():
    _write_item_list()
    _write_enhance_cost()
    _write_ascend_cost()
    _write_stat_curve_level()
    _write_stat_curve_ascension()


if __name__ == '__main__':
    # _debug_item_list()
    write_weapon_data()
