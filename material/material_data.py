from _data.i18n_json import *
from _utils.data_writer import *
from material.material_meta import *

item_type = 'material'


def _debug_item_list():
    for item in material_config_data:
        config_id = item['Id']
        desc = lang_zhs_config[str(item['DescTextMapHash'])]
        name = lang_zhs_config[str(item['NameTextMapHash'])]
        print(config_id, name, desc)


def _write_item_list():
    extracted_paimon = {}
    extracted_view = {}
    for item_id, item in get_material_list().items():
        config_id = item.get('Id', item_id)
        rarity = item.get('RankLevel', 1) if item.get('$type', '') != 'empty' else 3
        extracted = {
            'rarity': rarity
        }
        recipes = []
        for recipe_config in get_item_recipe(config_id):
            recipe = {}
            cost_mora = recipe_config.get('ScoinCost')
            if cost_mora:
                recipe[10001] = cost_mora
            for cm in recipe_config.get('MaterialItems', []):
                if cm != {}:
                    recipe[material_mapping[cm['Id']]] = cm['Count']
            recipes.append(recipe)
        if len(recipes) > 0:
            extracted['recipes'] = recipes
        extracted_paimon[item_id] = extracted
        view = {'gameId': item.get('Id')} | extracted
        if view['gameId'] is None:
            view.pop('gameId')
        extracted_view[item_id] = view
    write_data_json(item_type, 'list', extracted_paimon, extracted_view)


def _write_item_group():
    write_data_json(item_type, 'group', material_group_mapping)


def _write_item_type():
    write_data_json(item_type, 'type', material_type_mapping)


def _write_exp_items():
    extracted_paimon = {}
    item_list = get_material_list()
    for target, item_ids in exp_materials.items():
        extracted_paimon[target] = [{'id': item_id, 'exp': int(item_list[item_id]['ItemUse'][0]['UseParam'][0])}
                                    for item_id in item_ids]
    write_data_json(item_type, 'with-exp', extracted_paimon)


def write_material_data():
    _write_item_list()
    _write_item_group()
    _write_item_type()
    _write_exp_items()


if __name__ == '__main__':
    # _debug_item_list()
    write_material_data()
