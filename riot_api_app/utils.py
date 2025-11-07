def calculate_score(player_data, all_data):

    all_scores = get_all_scores("assists", all_data)
    assists = get_pos(player_data["assists"], all_scores) * 0.3

    all_scores = get_all_scores("damageSelfMitigated", all_data)
    damageSelfMitigated = get_pos(player_data["damageSelfMitigated"], all_scores) * 0.25

    all_scores = get_all_scores("deaths", all_data)
    deaths = (11 - get_pos(player_data["deaths"], all_scores)) * 0.2

    all_scores = get_all_scores("goldEarned", all_data)
    goldEarned = get_pos(player_data["goldEarned"], all_scores) * 0.5

    all_scores = get_all_scores("kills", all_data)
    kills = get_pos(player_data["kills"], all_scores) * 0.6

    all_scores = get_all_scores("totalDamageDealtToChampions", all_data)
    totalDamageDealtToChampions = (
        get_pos(player_data["totalDamageDealtToChampions"], all_scores) * 1
    )

    all_scores = get_all_scores("totalDamageShieldedOnTeammates", all_data)
    totalDamageShieldedOnTeammates = (
        get_pos(player_data["totalDamageShieldedOnTeammates"], all_scores) * 0.4
    )

    all_scores = get_all_scores("totalDamageTaken", all_data)
    totalDamageTaken = get_pos(player_data["totalDamageTaken"], all_scores) * 0.5

    all_scores = get_all_scores("totalHeal", all_data)
    totalHeal = get_pos(player_data["totalHeal"], all_scores) * 0.1

    all_scores = get_all_scores("totalHealsOnTeammates", all_data)
    totalHealsOnTeammates = (
        get_pos(player_data["totalHealsOnTeammates"], all_scores) * 0.4
    )

    all_scores = get_all_scores("timeCCingOthers", all_data)
    timeCCingOthers = get_pos(player_data["timeCCingOthers"], all_scores) * 0.3

    win = 0
    if player_data["win"]:
        win = 2

    score = (
        assists
        + damageSelfMitigated
        + deaths
        + goldEarned
        + kills
        + totalDamageDealtToChampions
        + totalDamageShieldedOnTeammates
        + totalDamageTaken
        + totalHeal
        + totalHealsOnTeammates
        + timeCCingOthers
        + win
    )

    return score


def get_pos(score, all_scores):
    pos = 10
    for player in all_scores:
        if score < player:
            pos -= 1
    return pos


def get_all_scores(cat, all_data):
    all_scores = []
    for player in all_data:
        all_scores.append(player[cat])
    return all_scores
