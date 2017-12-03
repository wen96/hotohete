class CSUserStatsService(object):
    PLAYED_PREFIX = 'total_rounds_map_'
    WINS_PREFIX = 'total_wins_map_'

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
    def users_by_elo(cls, users):
        return sorted(users, key=lambda user: cls.calculate_elo(user.csgo_info), reverse=True)

    @classmethod
    def calculate_elo(cls, csgo_info):
        if csgo_info:
            kills_min = cls.calculate_kills_min(csgo_info)
            wins_min = cls.calculate_wins_min(csgo_info)
            damage_min = cls.calculate_damage_min(csgo_info)
            wins_rate = float(csgo_info['total_wins']) * 100 / float(csgo_info['total_rounds_played'])
            kills_round = cls.calculate_kills_round(csgo_info)
            wins_round = cls.calculate_wins_round(csgo_info)
            damage_round = cls.calculate_damage_round(csgo_info)
            wins_rate_ponderate = wins_rate * 10
            score_per_second = cls.calculate_score_per_second(csgo_info)
            return sum([kills_min, wins_min, damage_min, wins_rate, kills_round, wins_round,
                        damage_round, wins_rate_ponderate, score_per_second]) / 20.0
        return 0

    @classmethod
    def calculate_kills_min(cls, csgo_info):
        return float(csgo_info['total_kills']) / float(csgo_info['total_time_played'])

    @classmethod
    def calculate_wins_min(cls, csgo_info):
        return float(csgo_info['total_wins']) / float(csgo_info['total_time_played'])

    @classmethod
    def calculate_damage_min(cls, csgo_info):
        return float(csgo_info['total_damage_done']) / float(csgo_info['total_time_played'])

    @classmethod
    def calculate_kills_round(cls, csgo_info):
        return float(csgo_info['total_kills']) / float(csgo_info['total_rounds_played'])

    @classmethod
    def calculate_wins_round(cls, csgo_info):
        return float(csgo_info['total_wins']) / float(csgo_info['total_rounds_played'])

    @classmethod
    def calculate_damage_round(cls, csgo_info):
        return float(csgo_info['total_damage_done']) / float(csgo_info['total_rounds_played'])

    @classmethod
    def calculate_score_per_second(cls, csgo_info):
        return float(csgo_info['total_contribution_score']) / float(csgo_info['total_time_played'])

    @classmethod
    def calculate_maps_stats(cls, csgo_info):
        maps_stats = {}
        if csgo_info:
            total_played = 0
            total_wins = 0
            for stat_key in csgo_info.keys():
                map_name = cls.get_map_name_from_stat_key(stat_key)

                if map_name and map_name not in maps_stats:
                    map_stats = cls._calculate_map_stat(csgo_info, map_name)
                    total_played += map_stats['played']
                    total_wins += map_stats['wins']
                    maps_stats[map_name] = map_stats

            unknown_played = csgo_info['total_rounds_played'] - total_played
            unknown_wins = csgo_info['total_wins'] - total_wins
            maps_stats['unknown'] = {
                'played': unknown_played,
                'wins': unknown_wins,
                'lost': unknown_played - unknown_wins
            }
        return maps_stats

    @classmethod
    def _calculate_map_stat(cls, csgo_info, map_name):
        played = csgo_info.get('{}{}'.format(cls.PLAYED_PREFIX, map_name), 0)
        wins = csgo_info.get('{}{}'.format(cls.WINS_PREFIX, map_name), 0)

        # Sometime we not receive total rounds played we we assume wins as played
        if wins > played:
            played = wins

        return {
            'played': played,
            'wins': wins,
            'lost': played - wins
        }

    @classmethod
    def get_map_name_from_stat_key(cls, stat_key):
        if stat_key.startswith(cls.PLAYED_PREFIX):
            return stat_key.split(cls.PLAYED_PREFIX)[-1]
        elif stat_key.startswith(cls.WINS_PREFIX):
            return stat_key.split(cls.WINS_PREFIX)[-1]

    @classmethod
    def users_by_hours_max_hours(cls, users):
        return sorted(users, key=lambda user: user.csgo_info.get('total_time_played', 0), reverse=True)
