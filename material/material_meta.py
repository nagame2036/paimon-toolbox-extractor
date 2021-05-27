import functools
from enum import IntEnum

from _data.data_json import *
from _utils.utils import sort_dict


class MaterialType(IntEnum):
    CURRENCY = 10
    GACHA = 11

    ORE = 20
    LOCAL_SPECIALTY = 21
    EQUIPMENT_BILLET = 22
    INGREDIENT = 23
    POTION = 24
    FOOD = 25

    ENEMY_MOB = 31
    ENEMY_ELITE = 32

    CHARACTER_COMMON = 40
    CHARACTER_BOSS = 41
    CHARACTER_GEM = 42

    TALENT_COMMON = 50,
    TALENT_147 = 51
    TALENT_257 = 52
    TALENT_367 = 53

    WEAPON_COMMON = 60
    WEAPON_147 = 61
    WEAPON_257 = 62
    WEAPON_367 = 63

    ARTIFACT_COMMON = 70


material_list = {
    MaterialType.CURRENCY: {
        202: 10001,  # 摩拉
    },
    MaterialType.GACHA: {
        201: 11001,  # 原石
        224: 11002,  # 相遇之缘
        223: 11003,  # 纠缠之缘
    },
    MaterialType.ORE: {
        101001: 20101,  # 铁块
        101002: 20102,  # 白铁块
        101003: 20103,  # 水晶块
        101004: 20104,  # 魔晶块
        101006: 20106,  # 星银矿石
    },
    MaterialType.LOCAL_SPECIALTY: {
        100021: 21001,  # 钩钩果
        100022: 21002,  # 落落莓
        100023: 21003,  # 塞西莉亚花
        100024: 21004,  # 风车菊
        100025: 21005,  # 慕风蘑菇
        100055: 21006,  # 小灯草
        100056: 21007,  # 嘟嘟莲
        100057: 21008,  # 蒲公英籽
        100027: 21009,  # 绝云椒椒
        100028: 21010,  # 夜泊石
        100029: 21011,  # 霓裳花
        100030: 21012,  # 琉璃百合
        100031: 21013,  # 清心
        100033: 21014,  # 星螺
        100034: 21015,  # 琉璃袋
        100058: 21016,  # 石珀
    },
    MaterialType.ENEMY_MOB: {
        112002: 31001,  # 史莱姆凝液
        112003: 31002,  # 史莱姆清
        112004: 31003,  # 史莱姆原浆
        112005: 31004,  # 破损的面具
        112006: 31005,  # 污秽的面具
        112007: 31006,  # 不祥的面具
        112008: 31007,  # 导能绘卷
        112009: 31008,  # 封魔绘卷
        112010: 31009,  # 禁咒绘卷
        112011: 31010,  # 牢固的箭簇
        112012: 31011,  # 锐利的箭簇
        112013: 31012,  # 历战的箭簇
        112032: 31013,  # 新兵的徽记
        112033: 31014,  # 士官的徽记
        112034: 31015,  # 尉官的徽记
        112035: 31016,  # 寻宝鸦印
        112036: 31017,  # 藏银鸦印
        112037: 31018,  # 攫金鸦印
        112038: 31019,  # 骗骗花蜜
        112039: 31020,  # 微光花蜜
        112040: 31021,  # 原素花蜜
    },
    MaterialType.ENEMY_ELITE: {
        112014: 32001,  # 沉重号角
        112015: 32002,  # 黑铜号角
        112016: 32003,  # 黑晶号角
        112020: 32004,  # 地脉的旧枝
        112021: 32005,  # 地脉的枯叶
        112022: 32006,  # 地脉的新芽
        112023: 32007,  # 混沌装置
        112024: 32008,  # 混沌回路
        112025: 32009,  # 混沌炉心
        112026: 32010,  # 雾虚花粉
        112027: 32011,  # 雾虚草囊
        112028: 32012,  # 雾虚灯芯
        112029: 32013,  # 猎兵祭刀
        112030: 32014,  # 特工祭刀
        112031: 32015,  # 督察长祭刀
        112041: 32016,  # 脆弱的骨片
        112042: 32017,  # 结实的骨片
        112043: 32018,  # 石化的骨片
    },
    MaterialType.CHARACTER_COMMON: {
        101: 40001,  # 角色经验
        104001: 40101,  # 流浪者的经验
        104002: 40102,  # 冒险家的经验
        104003: 40103,  # 大英雄的经验
    },
    MaterialType.CHARACTER_BOSS: {
        113001: 41001,  # 飓风之种
        113009: 41002,  # 玄岩之塔
        113002: 41003,  # 雷光棱镜
        113012: 41005,  # 净水之心
        113011: 41006,  # 常燃火种
        113010: 41007,  # 极寒之核
        113016: 41008,  # 未熟之玉
        113020: 41009,  # 晶凝之华
    },
    MaterialType.CHARACTER_GEM: {
        104201: 42001,  # 嬗变之尘
        104101: 42101,  # 璀璨原钻碎屑
        104102: 42102,  # 璀璨原钻断片
        104103: 42103,  # 璀璨原钻块
        104104: 42104,  # 璀璨原钻
        104151: 42105,  # 自在松石碎屑
        104152: 42106,  # 自在松石断片
        104153: 42107,  # 自在松石块
        104154: 42108,  # 自在松石
        104171: 42109,  # 坚牢黄玉碎屑
        104172: 42110,  # 坚牢黄玉断片
        104173: 42111,  # 坚牢黄玉块
        104174: 42112,  # 坚牢黄玉
        104141: 42113,  # 最胜紫晶碎屑
        104142: 42114,  # 最胜紫晶断片
        104143: 42115,  # 最胜紫晶块
        104144: 42116,  # 最胜紫晶
        # 104131: 42117,  # 生长碧翡碎屑
        # 104132: 42118,  # 生长碧翡断片
        # 104133: 42119,  # 生长碧翡块
        # 104134: 42120,  # 生长碧翡
        104121: 42121,  # 涤净青金碎屑
        104122: 42122,  # 涤净青金断片
        104123: 42123,  # 涤净青金块
        104124: 42124,  # 涤净青金
        104111: 42125,  # 燃愿玛瑙碎屑
        104112: 42126,  # 燃愿玛瑙断片
        104113: 42127,  # 燃愿玛瑙块
        104114: 42128,  # 燃愿玛瑙
        104161: 42129,  # 哀叙冰玉碎屑
        104162: 42130,  # 哀叙冰玉断片
        104163: 42131,  # 哀叙冰玉块
        104164: 42132,  # 哀叙冰玉
    },
    MaterialType.TALENT_COMMON: {
        104319: 50001,  # 智识之冕
        113021: 50002,  # 异梦溶媒
        113003: 50101,  # 东风之翎
        113004: 50102,  # 东风之爪
        113005: 50103,  # 东风的吐息
        113006: 50104,  # 北风之尾
        113007: 50105,  # 北风之环
        113008: 50106,  # 北风的魂匣
        113013: 50107,  # 吞天之鲸·只角
        113014: 50108,  # 魔王之刃·残片
        113015: 50109,  # 武炼之魂·孤影
        113017: 50110,  # 龙王之冕
        113018: 50111,  # 血玉之枝
        113019: 50112,  # 鎏金之鳞
    },
    MaterialType.TALENT_147: {
        104301: 51001,  # 「自由」的教导
        104302: 51002,  # 「自由」的指引
        104303: 51003,  # 「自由」的哲学
        104310: 51004,  # 「繁荣」的教导
        104311: 51005,  # 「繁荣」的指引
        104312: 51006,  # 「繁荣」的哲学
    },
    MaterialType.TALENT_257: {
        104304: 52001,  # 「抗争」的教导
        104305: 52002,  # 「抗争」的指引
        104306: 52003,  # 「抗争」的哲学
        104313: 52004,  # 「勤劳」的教导
        104314: 52005,  # 「勤劳」的指引
        104315: 52006,  # 「勤劳」的哲学
    },
    MaterialType.TALENT_367: {
        104307: 53001,  # 「诗文」的教导
        104308: 53002,  # 「诗文」的指引
        104309: 53003,  # 「诗文」的哲学
        104316: 53004,  # 「黄金」的教导
        104317: 53005,  # 「黄金」的指引
        104318: 53006,  # 「黄金」的哲学
    },
    MaterialType.WEAPON_COMMON: {
        -60001: 60001,  # 武器经验
        104011: 60101,  # 精锻用杂矿
        104012: 60102,  # 精锻用良矿
        104013: 60103,  # 精锻用魔矿
    },
    MaterialType.WEAPON_147: {
        114001: 61001,  # 高塔孤王的破瓦
        114002: 61002,  # 高塔孤王的残垣
        114003: 61003,  # 高塔孤王的断片
        114004: 61004,  # 高塔孤王的碎梦
        114013: 61005,  # 孤云寒林的光砂
        114014: 61006,  # 孤云寒林的辉岩
        114015: 61007,  # 孤云寒林的圣骸
        114016: 61008,  # 孤云寒林的神体
    },
    MaterialType.WEAPON_257: {
        114017: 62001,  # 雾海云间的铅丹
        114018: 62002,  # 雾海云间的汞丹
        114019: 62003,  # 雾海云间的金丹
        114020: 62004,  # 雾海云间的转还
        114005: 62005,  # 凛风奔狼的始龀
        114006: 62006,  # 凛风奔狼的裂齿
        114007: 62007,  # 凛风奔狼的断牙
        114008: 62008,  # 凛风奔狼的怀乡
    },
    MaterialType.WEAPON_367: {
        114009: 63001,  # 狮牙斗士的枷锁
        114010: 63002,  # 狮牙斗士的铁链
        114011: 63003,  # 狮牙斗士的镣铐
        114012: 63004,  # 狮牙斗士的理想
        114021: 63005,  # 漆黑陨铁的一粒
        114022: 63006,  # 漆黑陨铁的一片
        114023: 63007,  # 漆黑陨铁的一角
        114024: 63008,  # 漆黑陨铁的一块
    },
    MaterialType.ARTIFACT_COMMON: {
        -70001: 70001,  # 圣遗物经验
        105002: 70102,  # 祝圣油膏
        105003: 70103,  # 祝圣精华
    }
}

material_mapping = {k: v for vs in material_list.values() for k, v in vs.items()}
material_mapping_reverse = {v: k for k, v in material_mapping.items()}

material_type_mapping = {k: list(vs.values()) for k, vs in material_list.items()}

exp_materials = {
    40001: [x for x in material_type_mapping[MaterialType.CHARACTER_COMMON] if 40100 < x < 40104],  # 角色经验
    60001: [x for x in material_type_mapping[MaterialType.WEAPON_COMMON] if 60100 < x < 60104],  # 武器经验
    70001: [x for x in material_type_mapping[MaterialType.ARTIFACT_COMMON] if 70100 < x < 70104],  # 圣遗物经验
}


def _get_group_chunk(size: int, items: list) -> list:
    return [items[i:i + size] for i in range(0, len(items), size)]


def _get_exp_group_chunk(exp_id: int) -> list:
    return [*exp_materials[exp_id], exp_id]


material_group_mapping = [
    *_get_group_chunk(3, material_type_mapping[MaterialType.ENEMY_MOB]),
    *_get_group_chunk(3, material_type_mapping[MaterialType.ENEMY_ELITE]),
    _get_exp_group_chunk(40001),
    *_get_group_chunk(4, [x for x in material_type_mapping[MaterialType.CHARACTER_GEM] if x > 42100]),
    *_get_group_chunk(3, material_type_mapping[MaterialType.TALENT_147]),
    *_get_group_chunk(3, material_type_mapping[MaterialType.TALENT_257]),
    *_get_group_chunk(3, material_type_mapping[MaterialType.TALENT_367]),
    _get_exp_group_chunk(60001),
    *_get_group_chunk(4, material_type_mapping[MaterialType.WEAPON_147]),
    *_get_group_chunk(4, material_type_mapping[MaterialType.WEAPON_257]),
    *_get_group_chunk(4, material_type_mapping[MaterialType.WEAPON_367]),
    _get_exp_group_chunk(70001),
]

_material_group_union_map = {}
for group in material_group_mapping:
    for material_id in group:
        _material_group_union_map[material_id] = group


@functools.lru_cache
def get_material_group_last(config_id: int) -> int:
    return _material_group_union_map.get(config_id, [config_id])[-1]


@functools.lru_cache
def get_material_group_index(config_id: int) -> int:
    return _material_group_union_map.get(config_id, [config_id]).index(config_id)


@functools.lru_cache
def get_material_list():
    items = {item_id: _get_item(config_id) for config_id, item_id in material_mapping.items()}
    return sort_dict(items)


@functools.lru_cache
def _get_item(config_id: int) -> dict:
    return next((x for x in material_config_data if x['Id'] == config_id), {'$type': 'empty'})


_craft_data = [*forge_config_data, *alchemy_config_data]


@functools.lru_cache
def get_item_recipe(config_id: int) -> [dict]:
    return [x for x in _craft_data if x.get('ResultItemId') == config_id]


def get_cost_items(config_ids: [dict]) -> list:
    return [{'id': material_mapping.get(x.get('Id')), 'count': x.get('Count', 0)} for x in config_ids]


def get_cost_detail(cost: dict) -> dict:
    return {
        'index': get_material_group_index(cost['id']),
        'count': cost['count'],
    }
