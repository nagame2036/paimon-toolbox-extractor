from _utils.i18n_writer import *
from artifact.artifact_meta import *


def _write_artifact():
    names = {item_id: item['NameTextMapHash'] for item_id, item in get_artifact_list().items()}
    write_i18n_mapping('artifact', names)


def _write_artifact_set():
    names = {item_id: info['abilities'][0]['meta']['name'] for item_id, info in get_artifact_set_list().items()}
    write_i18n_mapping('artifact-set', names)


def _write_artifact_ability_desc():
    names = {}
    for item_id, info in get_artifact_set_list().items():
        for ability in info['abilities']:
            names[f'{item_id}.{ability["require"]}'] = ability['meta']['desc']
    write_i18n_mapping('artifact-ability-desc', names)


def write_artifact_i18n():
    _write_artifact()
    _write_artifact_set()
    _write_artifact_ability_desc()
