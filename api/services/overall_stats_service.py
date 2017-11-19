from collections import defaultdict


class OverallStatsService(object):
    @classmethod
    def maps_stats_from_users(cls, users):
        map_stats = defaultdict(lambda: {'played': 0, 'wins': 0, 'lost': 0})
        for user in users:
            user_map_stats = user.maps_stats
            for map_name in user_map_stats.keys():
                map_stats[map_name]['played'] += user_map_stats[map_name]['played']
                map_stats[map_name]['wins'] += user_map_stats[map_name]['wins']
                map_stats[map_name]['lost'] += user_map_stats[map_name]['lost']

        return map_stats

    @classmethod
    def maps_by_played(cls, map_stats):
        map_list = []
        for map_name in map_stats.keys():
            stats = map_stats[map_name].copy()
            stats['name'] = map_name
            map_list.append(stats)
        return sorted(map_list, key=lambda map_stat: map_stat.get('played', 0), reverse=True)
