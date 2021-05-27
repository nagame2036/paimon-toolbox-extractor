from _spider import get_fandom_icon_urls, write_fandom_images
from _utils.utils import read_text_map
from element.element_meta import *


def _write_icon():
    items = read_text_map(element_mapping)
    urls = get_fandom_icon_urls(items)
    write_fandom_images('element', urls, file_map=lambda x: f'Element_{x}')


def write_element_image():
    _write_icon()


if __name__ == '__main__':
    write_element_image()
