class CSUserStatsService(object):

    @classmethod
    def calculate_category_weapons_kills(cls, csgo_info):
        weapons_kills = {}
        if csgo_info:
            smgs = ['p90', 'bizon', 'ump45', 'mp7', 'mp9']
            snipers = ['awp', 'ssg08']
            pistols = ['glock', 'deagle', 'elite', 'fiveseven', 'hkp2000', 'p250']
            rifles = ['ak47', 'm4a1', 'famas', 'galilar']
            shotguns = ['mag7', 'xm1014', 'nova', 'sawedoff']
            throwables = ['hegrenade', 'molotov']

            weapons_kills = {
                'smg': 0,
                'sniper': 0,
                'pistol': 0,
                'rifle': 0,
                'shotgun': 0,
                'throw': 0,
            }

            for smg in smgs:
                weapons_kills['smg'] += csgo_info['total_kills_{}'.format(smg)]

            for sniper in snipers:
                weapons_kills['sniper'] += csgo_info['total_kills_{}'.format(sniper)]

            for pistol in pistols:
                weapons_kills['pistol'] += csgo_info['total_kills_{}'.format(pistol)]

            for rifle in rifles:
                weapons_kills['rifle'] += csgo_info['total_kills_{}'.format(rifle)]

            for shotgun in shotguns:
                weapons_kills['shotgun'] += csgo_info['total_kills_{}'.format(shotgun)]

            for throwable in throwables:
                weapons_kills['throw'] += csgo_info['total_kills_{}'.format(throwable)]

            weapons_kills['other'] = csgo_info['total_kills'] - sum(weapons_kills.values())

        return weapons_kills
