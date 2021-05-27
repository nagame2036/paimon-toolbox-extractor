from _utils.image_writer import add_image_mapping
from character.character_meta import *


def _write_icon():
    url = 'https://upload-os-bbs.mihoyo.com/game_record/genshin/character_icon'
    prefix = 'UI_AvatarIcon_'
    images = {item_id: item["IconName"].removeprefix(prefix) for item_id, item in get_character_list().items()}
    add_image_mapping('character', images, f'{url}/{prefix}')


def write_character_image():
    _write_icon()
