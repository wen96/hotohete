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

    @property
    def csgo_info(self):
        if self.get_steam_id:
            cs_info = self.steam_service.get_cs_info(self.get_steam_id) or []
            return {stat['name']: stat['value'] for stat in cs_info}

    @property
    def category_weapons_kills(self):
        return CSUserStatsService.calculate_category_weapons_kills(self.csgo_info)

    @property
    def maps_stats(self):
        return CSUserStatsService.calculate_maps_stats(self.csgo_info)
