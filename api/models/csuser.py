from django.db import models
from api.services import SteamAPIService


class CSUser(models.Model):
    steam_username = models.CharField(max_length=255)
    team = models.ForeignKey('api.CSTeam', on_delete=models.SET_NULL, null=True)
    steam_id = models.CharField(max_length=126, null=True, blank=True)
    visible = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    csgo_info = None

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
    def get_steam_info(self):
        return self.steam_service.get_steam_info(self.get_steam_id)

    @property
    def get_cs_info(self):
        if not self.csgo_info:
            cs_info = self.steam_service.get_cs_info(self.get_steam_id) or []
            self.csgo_info = {stat['name']: stat['value'] for stat in cs_info}
        return self.csgo_info

    @property
    def category_weapons_kills(self):
        weapons_kills = {}
        if self.csgo_info:
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
                weapons_kills['smg'] += self.csgo_info['total_kills_{}'.format(smg)]

            for sniper in snipers:
                weapons_kills['sniper'] += self.csgo_info['total_kills_{}'.format(sniper)]

            for pistol in pistols:
                weapons_kills['pistol'] += self.csgo_info['total_kills_{}'.format(pistol)]

            for rifle in rifles:
                weapons_kills['rifle'] += self.csgo_info['total_kills_{}'.format(rifle)]

            for shotgun in shotguns:
                weapons_kills['shotgun'] += self.csgo_info['total_kills_{}'.format(shotgun)]

            for throwable in throwables:
                weapons_kills['throw'] += self.csgo_info['total_kills_{}'.format(throwable)]

            weapons_kills['other'] = self.csgo_info['total_kills'] - sum(weapons_kills.values())

        return weapons_kills
