from _utils.data_reader import *


def _read_config(file_name: str):
    return read_json(f'F:/Projects/genshin-impact/genshin-impact-data/TextMap/{file_name}.json')


lang_zhs_config = _read_config('TextCHS')
lang_en_config = _read_config('TextEN')
i18n_config = {
    'zh-hans': lang_zhs_config,
    'en': lang_en_config,
    'ja': _read_config('TextJA'),
}
