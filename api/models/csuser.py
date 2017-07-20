from django.db import models
from api.services import SteamAPIService


class CSUser(models.Model):
    steam_username = models.CharField(max_length=255)
    team = models.ForeignKey('api.CSTeam', on_delete=models.SET_NULL, null=True)
    steam_id = models.CharField(max_length=126, null=True, blank=True)

    steam_service = SteamAPIService()

    def __str__(self):
        return self.steam_username

    @property
    def get_steam_id(self):
        if not self.steam_id:
            self.steam_id = self.steam_service.get_steam_id_from_nick_name(self.steam_username)
            self.save()
        return self.steam_id

    @property
    def get_steam_info(self):
        return self.steam_service.get_steam_info(self.get_steam_id)

    @property
    def get_cs_info(self):
        return self.steam_service.get_cs_info(self.get_steam_id)

    @property
    def get_weapon_group_per(self):
        return self.steam_service.get_weapon_group_per(self.get_steam_id)
