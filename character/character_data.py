from _utils.data_writer import *
from character.character_meta import *
from material import *
from weapon import *

item_type = 'character'


def _debug_item_list():
    for item_id, item in get_character_list().items():
        item_name = lang_zhs_config[str(item['NameTextMapHash'])]
        print(item_id, item_name, item)


def _write_item_list():
    extracted_paimon = {}
    extracted_view = {}
    profile_list = get_profile_list()
    talent_list = get_talent_list()['items']
    constellation_list = get_constellation_list()
    for item_id, item in get_character_list().items():
        profile = profile_list[item_id]
        ascension_id = 'AvatarPromoteId'
        ascensions = [x for x in character_ascension_config_data if x[ascension_id] == item[ascension_id]]

        cost = [get_material_group_last(material_mapping.get(x.get('Id'))) for x in ascensions[-1]['CostItems']]
        materials = {
            'boss': cost[1],
            'gem': cost[0],
            'local': cost[2],
            'mob': cost[3],
        }
        if not materials['boss']:
            materials.pop('boss')

        curves = defaultdict(lambda: [])
        for ascension_config in ascensions:
            for stat_config in ascension_config['AddProps']:
                stat_type = stat_mapping[stat_config['PropType']]
                stat_value = to_float(stat_config.get('Value', 0))
                curves[stat_type].append(stat_value)

        talent = talent_list[item_id]
        extracted = {
            'rarity': rarity_mapping[item['QualityType']],
            'element': talent['element'],
            'weapon': weapon_type_mapping[item['WeaponType']],
            'region': region_mapping.get(profile['AvatarAssocType'], 0),
            'constellation': constellation_list[item_id]['id'],
            'talents': talent['talents'],
            'materials': materials,
            'stats': {
                'HP Base': get_curve_level(item, 'HpBase', 'HP Base'),
                'ATK Base': get_curve_level(item, 'AttackBase', 'ATK Base'),
                'DEF Base': get_curve_level(item, 'DefenseBase', 'DEF Base'),
            },
            'curves': {k: v for k, v in curves.items() if v},
        }
        if extracted['constellation'] == item_id:
            extracted.pop('constellation')

        extracted_paimon[item_id] = extracted
        extracted_view[item_id] = {'gameId': item['Id']} | extracted
    write_data_json(item_type, 'list', extracted_paimon, extracted_view)


def _write_levelup_cost():
    extracted_paimon = [x['Exp'] for x in character_levelup_cost_config_data]
    write_data_json(item_type, 'levelup-cost', extracted_paimon)


def _write_ascend_cost():
    extracted_paimon = []
    for item in character_ascension_config_data:
        cost = get_cost_items(item['CostItems'])
        if not cost[0]['id']:
            continue
        extracted = {
            'mora': item['ScoinCost'],
            'boss': cost[1]['count'],
            'gem': get_cost_detail(cost[0]),
            'local': cost[2]['count'],
            'mob': get_cost_detail(cost[3])
        }
        phase = item.get('PromoteLevel', 0)
        if len(extracted_paimon) < phase:
            extracted_paimon.append(extracted)
        elif extracted != extracted_paimon[phase - 1]:
            print(f'conflict ascension cost with id {item["AvatarPromoteId"]} ascension {phase}: {extracted}')
    write_data_json(item_type, 'ascend-cost', extracted_paimon)


def _write_curve_level():
    extracted_paimon = defaultdict(lambda: [])
    for level in character_stats_curve_config_data:
        for curve in level['CurveInfos']:
            stat_type = character_curve_level_mapping[curve['Type']]
            stat_value = to_float(curve['Value'])
            extracted_paimon[stat_type].append(stat_value)
    write_data_json(item_type, 'stat-curve-level', extracted_paimon)


def write_character_data():
    _write_item_list()
    _write_levelup_cost()
    _write_ascend_cost()
    _write_curve_level()


if __name__ == '__main__':
    _debug_item_list()
    write_character_data()
