PART_ENUM = (
    "头盔",
    "胸甲",
    "手套",
    "靴子",
    "护腿",
    "护符",
    "戒指",
    "弩",
    "双手剑",
    "剑",
    "斧",
    "双手斧",
    "长柄武器",
)
WEAPON_ENUM = ("弩", "双手剑", "剑", "斧", "双手斧", "长柄武器")


def get_part(item_details):
    for part in PART_ENUM:
        for detail in item_details:
            if part in detail:
                return part
    return "NotFound"


def is_legendary(item_details):
    for detail in item_details:
        if "传奇" in detail:
            return True
    return False


def is_ancestral(item_details):
    for detail in item_details:
        if "先祖" in detail:
            return True
    return False


def find_n_digt_from_back(detail, n):
    res = 0
    c = 0
    for i in range(len(detail) - 1, -1, -1):
        if detail[i].isnumeric():
            res = res + (int(detail[i]) * (10**c))
            c += 1
            if c >= n:
                return res
    return res


def get_power(item_detils_str):
    endpos = item_detils_str.find("物品强度")
    power = find_n_digt_from_back(item_detils_str[0:endpos], 3)
    return power


def get_stats(item_detils_str):
    return item_detils_str


def get_attributes(item_details):
    item_detils_str = "".join(item_details)
    part = get_part(item_details)
    legendary = is_legendary(item_details)
    ancestral = is_ancestral(item_details)
    power = get_power(item_detils_str)
    stats = get_stats(item_detils_str)

    return (part, legendary, ancestral, power, stats)


def is_junk(item_details, claz, sub):
    print("\nEvaluating item for class: " + claz + "Item Details: ")
    print(item_details)

    part, legendary, ancestral, power, stats = get_attributes(item_details)

    print("Part: " + part)
    print("Is Legendary? " + str(legendary))
    print("Is Ancestral? " + str(ancestral))
    print("Item Power: " + str(power))

    # Any legendary items can be useful
    if legendary:
        return False

    # Drop non ancestral items
    if not ancestral:
        return True

    # Drop low power weapons
    if part in WEAPON_ENUM:
        if power < 720:
            return True

    return evaluate_stats(part, stats)


stats_ranking = {
    "头盔": {"must": ["冷却"], "t0": ["死亡重击"]},
    "胸甲": {"must": [], "t0": ["伤害减免"]},
    "护腿": {"must": [], "t0": ["伤害减免"]},
    "手套": {"must": ["扬石飞沙"], "t0": ["暴击", "攻击速度", "幸运一击"]},
    "靴子": {"must": ["移动速度"], "t0": ["冷却"]},
    "护符": {"must": ["势大力沉"], "t0": ["移动速度", "冷却"]},
    "戒指": {"must": [], "t0": ["暴击", "力量", "易伤"]},
    "武器": {"must": [], "t0": ["暴击", "力量", "易伤"]},
}


def evaluate_stats(part, stats):
    score = 0
    if part in WEAPON_ENUM:
        part = "武器"
    ranking = stats_ranking[part]
    for must in ranking["must"]:
        if must not in stats:
            return True
    for t0 in ranking["t0"]:
        if t0 in stats:
            score += 1

    if score > 0:
        return False

    return True
