from _spider import get_fandom_icon_urls, write_fandom_images
from material.material_meta import *

_icon_defaults = {
    10001: '8/84/Icon_Mora',
    32006: '2/22/Item_Ley_Line_Sprouts'
}


def _write_icon():
    items = {item_id: item['NameTextMapHash'] for item_id, item in get_material_list().items() if
             item.get('$type') != 'empty'}
    urls = get_fandom_icon_urls(items)
    write_fandom_images('material', urls, _icon_defaults, file_map=lambda x: f'Item_{x}')


def write_material_image():
    _write_icon()


if __name__ == '__main__':
    _write_icon()
