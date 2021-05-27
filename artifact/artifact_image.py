from _spider import get_fandom_icon_urls, write_fandom_images
from _utils.image_writer import add_image_mapping
from artifact.artifact_meta import *


def _write_icon():
    url = 'https://upload-os-bbs.mihoyo.com/game_record/genshin/equip'
    prefix = 'UI_RelicIcon_'
    images = {item_id: item["Icon"].removeprefix(prefix) for item_id, item in get_artifact_list().items()}
    add_image_mapping('artifact', images, f'{url}/{prefix}')


def _write_type():
    items = read_text_map(artifact_type_mapping)
    urls = get_fandom_icon_urls(items)
    write_fandom_images('artifact-type', urls, file_map=lambda x: f'Icon_{x}')


def write_artifact_image():
    _write_icon()
    _write_type()
