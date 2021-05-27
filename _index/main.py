import artifact
import character
import element
import material
import weapon
import constellation
import talent
from _utils.i18n_writer import write_i18n_json
from _utils.image_writer import write_image_json, save_remote_image


def extract_data():
    material.write_data()
    character.write_data()
    constellation.write_data()
    talent.write_data()
    weapon.write_data()
    artifact.write_data()


def extract_i18n():
    material.write_i18n()
    character.write_i18n()
    constellation.write_i18n()
    talent.write_i18n()
    weapon.write_i18n()
    artifact.write_i18n()
    write_i18n_json()


def extract_image():
    element.write_image()
    material.write_image()
    character.write_image()
    weapon.write_image()
    artifact.write_image()
    write_image_json()


if __name__ == '__main__':
    extract_data()
    extract_i18n()
    extract_image()
    save_remote_image()
