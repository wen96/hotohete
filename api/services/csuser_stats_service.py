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

    @classmethod
    def calculate_maps_stats(cls, csgo_info):
        maps_stats = {}
        if csgo_info:
            played_prefix = 'total_rounds_map_'
            wins_prefix = 'total_wins_map_'
            total_played = 0
            total_wins = 0
            for stat_key in csgo_info.keys():
                map_name = None
                if stat_key.startswith(played_prefix):
                    map_name = stat_key.split(played_prefix)[-1]
                elif stat_key.startswith(wins_prefix):
                    map_name = stat_key.split(wins_prefix)[-1]

                if map_name and map_name not in maps_stats:
                    played = csgo_info.get('{}{}'.format(played_prefix, map_name), 0)
                    wins = csgo_info.get('{}{}'.format(wins_prefix, map_name), 0)

                    # Sometime we not receive total rounds played we we assume wins as played
                    if wins > played:
                        played = wins

                    total_played += played
                    total_wins += wins
                    maps_stats[map_name] = {
                        'played': played,
                        'wins': wins,
                        'lost': played - wins
                    }

            unknown_played = csgo_info['total_rounds_played'] - total_played
            unknown_wins = csgo_info['total_wins'] - total_wins
            maps_stats['unknown'] = {
                'played': unknown_played,
                'wins': unknown_wins,
                'lost': unknown_played - unknown_wins
            }
        return maps_stats

    @classmethod
    def users_by_hours_max_hours(cls, users):
        return sorted(users, key=lambda user: user.csgo_info.get('total_time_played', 0), reverse=True)
