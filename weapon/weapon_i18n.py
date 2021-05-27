from _utils.i18n_writer import *
from weapon.weapon_meta import *


def _write_weapon():
    names = {item_id: info['item']['NameTextMapHash'] for item_id, info in get_weapon_list().items()}
    write_i18n_mapping('weapon', names)


def _write_weapon_ability():
    names = {item_id: info['ability']['meta']['name'] for item_id, info in get_weapon_list().items()}
    write_i18n_mapping('weapon-ability', names)


def _write_weapon_ability_desc():
    names = {item_id: info['ability']['meta']['desc'] for item_id, info in get_weapon_list().items()}
    write_i18n_mapping('weapon-ability-desc', names, map_func=replace_color)


def write_weapon_i18n():
    _write_weapon()
    _write_weapon_ability()
    _write_weapon_ability_desc()
