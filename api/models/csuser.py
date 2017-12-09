from django.db import models
from api.services.steam_api_service import SteamAPIService
from api.services.csuser_stats_service import CSUserStatsService


class CSUser(models.Model):
    steam_username = models.CharField(max_length=255)
    team = models.ForeignKey('api.CSTeam', on_delete=models.SET_NULL, null=True)
    steam_id = models.CharField(max_length=126, null=True, blank=True)
    visible = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    steam_service = SteamAPIService()

    ELO_SCALE = {
        30: 'Do not play with me',
        31: 'Ruski noob',
        32: 'Still noob ',
        33: 'Noob',
        34: 'Noob thinking he\'s a pro',
        35: 'Average shitty player',
        36: 'CSGO is my live',
        37: 'Pro Rusky killer',
        38: 'Master Rusky',
        39: 'Universe pro',
        40: 'Master of universe 1',
        41: 'Master of universe 2',
        42: 'Master of universe 3',
        43: 'Master of universe 4',
        44: 'You gonna die',
    }

    class Meta(object):
        ordering = ['order']

    def __str__(self):
        return self.steam_username

    @property
    def get_steam_id(self):
        if not self.steam_id:
            self.steam_id = self.steam_service.get_steam_id_from_nick_name(self.steam_username)
            self.save()
        return self.steam_id

    @property
    def steam_info(self):
        if self.get_steam_id:
            return self.steam_service.get_steam_info(self.get_steam_id)
        return {}

    @property
    def csgo_info(self):
        if self.get_steam_id:
            cs_info = self.steam_service.get_cs_info(self.get_steam_id) or []
            return {stat['name']: stat['value'] for stat in cs_info}
        return {}

    @property
    def category_weapons_kills(self):
        return CSUserStatsService.calculate_category_weapons_kills(self.csgo_info)

    @property
    def maps_stats(self):
        return CSUserStatsService.calculate_maps_stats(self.csgo_info)

    @property
    def elo(self):
        return CSUserStatsService.calculate_elo(self.csgo_info)

    @property
    def humanized_elo(self):
        elo = self.elo
        if elo > 43:
            elo = 40
        elif elo < 31:
            elo = 30
        return self.ELO_SCALE[int(elo)]

    @property
    def kill_death_ratio(self):
        return CSUserStatsService.calculate_kill_death_ratio(self.csgo_info)

    @property
    def weapon_stats(self):
        return CSUserStatsService.calculate_weapon_stats(self.csgo_info)

    @property
    def kills_min(self):
        return CSUserStatsService.calculate_kills_min(self.csgo_info)

    @property
    def wins_min(self):
        return CSUserStatsService.calculate_wins_min(self.csgo_info)

    @property
    def damanage_min(self):
        return CSUserStatsService.calculate_damage_min(self.csgo_info)

    @property
    def kills_round(self):
        return CSUserStatsService.calculate_kills_round(self.csgo_info)

    @property
    def wins_round(self):
        return CSUserStatsService.calculate_wins_round(self.csgo_info)

    @property
    def damange_round(self):
        return CSUserStatsService.calculate_damage_round(self.csgo_info)

    @property
    def score_per_second(self):
        return CSUserStatsService.calculate_score_per_second(self.csgo_info)

    @property
    def wins_rate(self):
        return float(self.csgo_info['total_wins']) * 100 / float(self.csgo_info['total_rounds_played'])
