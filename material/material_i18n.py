from _utils.i18n_writer import write_i18n_mapping
from material.material_meta import *


def _write_material():
    names = {item_id: item.get('NameTextMapHash') for item_id, item in get_material_list().items()}
    write_i18n_mapping('material', names, {
        60001: {
            'zh-hans': '武器经验',
            'en': 'Weapon EXP',
            'ja': '武器経験値',
        },
        70001: {
            'zh-hans': '圣遗物经验',
            'en': 'Artifact EXP',
            'ja': '聖遺物経験値',
        },
    })


def write_material_i18n():
    _write_material()
