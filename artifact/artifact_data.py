from collections import defaultdict

from _data.i18n_json import *
from _utils.data_writer import *
from artifact.artifact_meta import *
from stat_type import *

_output = 'artifact'


def _debug_set_list():
    for set_id, set_info in get_artifact_set_list().items():
        abilities = set_info['abilities']
        set_name = lang_zhs_config[str(abilities[0]['meta']['name'])]
        print(set_id, set_name, set_info)


def _write_set_list():
    extracted_paimon = {}
    extracted_view = {}
    for item_id, info in get_artifact_set_list().items():
        types = info['types']
        extracted = {
            'rarities': list(info['rarities']),
            'onlyTypes': types,
            'abilities': [{k: v for k, v in x.items() if k != 'meta'} for x in info['abilities']],
        }
        if len(types) == len(artifact_type_mapping):
            extracted.pop('onlyTypes')
        extracted_paimon[item_id] = extracted
        extracted_view[item_id] = {'gameId': info['set']['SetId']} | extracted
    write_data_json(_output, 'set-list', extracted_paimon, extracted_view)


_levels = [(x['Rank'], x) for x in artifact_level_config_data if x.get('Rank', 0) >= min_artifact_rarity]


def _write_enhance_cost():
    extracted_paimon = defaultdict(lambda: [])
    for rarity, item in _levels:
        extracted_paimon[rarity].append(item['Exp'])
    write_data_json(_output, 'enhance-cost', extracted_paimon)


def _write_enhance_exp_multipliers():
    extracted_paimon = {x['PowerupMultiple']: x['PowerupWeight'] for x in artifact_enhance_exp_multipliers_config_data}
    write_data_json(_output, 'enhance-exp-multipliers', extracted_paimon)


def _write_main_stat_curve_level():
    extracted_paimon = defaultdict(lambda: defaultdict(lambda: []))
    for rarity, item in _levels:
        for stat in item['AddProps']:
            stat_type = stat_mapping[stat['PropType']]
            stat_value = to_float(stat['Value'])
            extracted_paimon[rarity][stat_type].append(stat_value)
    write_data_json(_output, 'main-stat-curve-level', extracted_paimon)


_items_list = [(item_type, item) for info in get_artifact_set_list().values()
               for item_type, item in info['items'].items()]


def _write_main_stat_roll_weights():
    extracted_paimon = defaultdict(lambda: {})
    for item_type, item in _items_list:
        roll_pool = (x for x in artifact_main_stat_roll_config_data if x['PropDepotId'] == item['MainPropDepotId'])
        extracted = {stat_mapping[x['PropType']]: x['Weight'] for x in roll_pool if x.get('Weight')}
        if item_type not in extracted_paimon:
            extracted_paimon[item_type] = extracted
        elif extracted != extracted_paimon[item_type]:
            print(f'conflict main stat rolls on artifact id {item["Id"]} type {item_type}: {extracted}')
    write_data_json(_output, 'main-stat-roll-weights', extracted_paimon)


def _get_sub_stat_roll_pools(config_id: int):
    return [x for x in artifact_sub_stat_config_data if x['DepotId'] == config_id]


_sub_stat_pools = {item['RankLevel']: _get_sub_stat_roll_pools(item['AppendPropDepotId']) for _, item in _items_list}


def _write_sub_stat_values():
    extracted_paimon = defaultdict(lambda: defaultdict(lambda: []))
    for rarity, pools in _sub_stat_pools.items():
        for pool in pools:
            stat_type = stat_mapping[pool['PropType']]
            extracted_paimon[rarity][stat_type].append(to_float(pool['PropValue']))
    write_data_json(_output, 'sub-stat-values', extracted_paimon)


def _write_sub_stat_roll_weights():
    extracted_paimon = defaultdict(lambda: defaultdict(lambda: []))
    for rarity, pools in _sub_stat_pools.items():
        for pool in pools:
            stat_type = stat_mapping[pool['PropType']]
            extracted_paimon[rarity][stat_type].append(pool['Weight'])
    write_data_json(_output, 'sub-stat-roll-weights', extracted_paimon)


def _write_sub_stat_upgrade_weights():
    extracted_paimon = defaultdict(lambda: defaultdict(lambda: []))
    for rarity, pools in _sub_stat_pools.items():
        for pool in pools:
            stat_type = stat_mapping[pool['PropType']]
            extracted_paimon[rarity][stat_type].append(pool['UpgradeWeight'])
    write_data_json(_output, 'sub-stat-upgrade-weights', extracted_paimon)


def write_artifact_data():
    _write_set_list()
    _write_enhance_cost()
    _write_enhance_exp_multipliers()
    _write_main_stat_curve_level()
    _write_main_stat_roll_weights()
    _write_sub_stat_values()
    _write_sub_stat_roll_weights()
    _write_sub_stat_upgrade_weights()


if __name__ == '__main__':
    # _debug_set_list()
    write_artifact_data()
