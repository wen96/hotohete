from django.db import models
from api.services import SteamAPIService


class CSUser(models.Model):
    steam_username = models.CharField(max_length=255)
    team = models.ForeignKey('api.CSTeam', on_delete=models.SET_NULL, null=True)
    steam_id = models.CharField(max_length=126, null=True, blank=True)
    csgo_info = None

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
        if not self.csgo_info:
            self.csgo_info = {stat['name']: stat['value'] for stat in self.steam_service.get_cs_info(self.get_steam_id)}
        return self.csgo_info

    @property
    def category_weapons_kills(self):
        """ {'total_kills_p90': 123, 'total_kills_awp': 33}

            {
                'p90': 123,
                'awp': 123
            }
        """
        weapons_kills = {}

        smgs = ['p90', 'bizon', 'ump45', 'mp7', 'mp9']
        snipers = ['awp', 'ssg08']
        pistols = ['glock', 'deagle', 'elite', 'fiveseven', 'hkp2000', 'p250']
        rifles = ['ak47', 'm4a1', 'famas', 'galilar']
        shotguns = ['mag7', 'xm1014', 'nova', 'sawedoff']

        weapons_kills = {
            'smg': 0,
            'sniper': 0,
            'pistol': 0,
            'rifle': 0,
            'shotgun': 0,
        }

        for smg in smgs:
            weapons_kills['smg'] += self.csgo_info['total_kills_{}'.format(smg)]

        for smg in snipers:
            weapons_kills['sniper'] += self.csgo_info['total_kills_{}'.format(smg)]

        for smg in pistols:
            weapons_kills['pistol'] += self.csgo_info['total_kills_{}'.format(smg)]

        for smg in rifles:
            weapons_kills['rifle'] += self.csgo_info['total_kills_{}'.format(smg)]

        for smg in shotguns:
            weapons_kills['shotgun'] += self.csgo_info['total_kills_{}'.format(smg)]

        weapons_kills['other'] = self.csgo_info['total_kills'] - sum(weapons_kills.values())

        return weapons_kills
