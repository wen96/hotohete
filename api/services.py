import urllib2
import json
from api.models.hotohete_settings import HotoheteSettings


class SteamAPIService(object):

    def __init__(self):
        self._api_key = None
        self.base_url = 'http://api.steampowered.com'
        self.cache_steam_info = {}

    @property
    def api_key(self):
        if not self._api_key:
            self._api_key = HotoheteSettings.objects.get(key='STEAM_API_KEY').value
        return self._api_key

    def get_steam_id_from_nick_name(self, nickname):
        """Returns the steam id from nickname.
        """
        url = "{}/ISteamUser/ResolveVanityURL/v0001/".format(self.base_url)
        url_params = "?key={}&vanityurl={}".format(self.api_key, nickname)

        json_object = self._request_endpoint("{}{}".format(url, url_params))
        return json_object["response"].get("steamid")

    def get_steam_info(self, steam_id):
        # TODO: Use a cache with TTL (time to live)
        """Create the steam info for cache if not exists.
        If cs profile not founded, set cache to none.
        """
        if steam_id not in self.cache_steam_info:
            url = "{}/ISteamUser/GetPlayerSummaries/v0002/".format(self.base_url)
            url_params = "?key={}&steamids={}".format(self.api_key, steam_id)

            json_object = self._request_endpoint("{}{}".format(url, url_params))

            if json_object and json_object["response"]["players"]:
                self.cache_steam_info[steam_id] = json_object["response"]["players"][0]
            else:
                self.cache_steam_info[steam_id] = None

        return self.cache_steam_info[steam_id]

    def get_cs_info(self, steam_id):
        """ Returns none if steam_id not founded. If not, returns a json object which contains the CSplayer stats
        from def _request_endpoint or none if cs player not founded.
        """
        if steam_id:
            url = "{}/ISteamUserStats/GetUserStatsForGame/v0002/".format(self.base_url)
            url_params = "?appid=730&key={}&steamid={}".format(self.api_key, steam_id)

            json_object = self._request_endpoint("{}{}".format(url, url_params))

            return json_object["playerstats"]["stats"] if json_object else None
        return None

    def _request_endpoint(self, url):
        """ Returns an object loaded from a response expecting json response. None if 500 error.
        """
        try:
            response = urllib2.urlopen(url)
            return json.loads(response.read())
        except urllib2.HTTPError:

            return None

    def get_weapon_group_per(self, steam_id):
        # TODO: Refactor
        """ Returns an object which contains kills percentage ordered by group of weapons
        """
        percentage_weapons = {}
        json_object = self.get_cs_info(steam_id)

        if json_object:
            total_kills = json_object[0]["value"]

            kills_pistol = json_object[11]["value"]  # glock
            kills_pistol += json_object[135]["value"]  # usp/p2000
            kills_pistol += json_object[139]["value"]  # p250
            kills_pistol += json_object[168]["value"]  # tec
            kills_pistol += json_object[14]["value"]  # five7
            kills_pistol += json_object[13]["value"]  # dual berettas

            percentage_weapons["pistols"] = (total_kills / kills_pistol) * 100

            kills_shotgun = json_object[157]["value"]  # nova
            kills_shotgun += json_object[15]["value"]  # XM
            kills_shotgun += json_object[173]["value"]  # mag-7
            kills_shotgun += json_object[163]["value"]  # sawed

            percentage_weapons["shotguns"] = (total_kills / kills_shotgun) * 100

            kills_sniper = json_object[19]["value"]  # awp
            kills_sniper += json_object[149]["value"]  # matapatos
            kills_sniper += json_object[12]["value"]  # deagle

            percentage_weapons["snipers"] = (total_kills / kills_sniper) * 100

            kills_rifle = json_object[20]["value"]  # AK-47
            kills_rifle += json_object[176]["value"]  # M4
            kills_rifle += json_object[22]["value"]  # FAMAS
            kills_rifle += json_object[177]["value"]  # GALIL

            percentage_weapons["rifles"] = (total_kills / kills_rifle) * 100

            kills_smg = json_object[152]["value"]  # mp7
            kills_smg += json_object[153]["value"]  # mp9
            kills_smg += json_object[16]["value"]  # MAC-10
            kills_smg += json_object[17]["value"]  # ump
            kills_smg += json_object[167]["value"]  # bizon

            percentage_weapons["smgs"] = (total_kills / kills_smg) * 100

            percentage_weapons["knife"] = json_object[9]["value"]

            percentage_weapons["tazer"] = json_object[179]["value"]

            kills_throwable = json_object[10]["value"]  # HE
            kills_throwable += json_object[178]["value"]  # molotov

            percentage_weapons["throwable"] = (total_kills / kills_throwable) * 100

            base = percentage_weapons["pistols"]["smg"]["snipers"]["rifles"]["shotguns"]["knife"]["tazer"]["throwable"]
            percentage_weapons["trash"] = base / 100

            return percentage_weapons

        else:
            return None


"""    def get_weapon_group_per(self, steam_id, weapon):
        # TODO: Refactor

        json_object = self.get_cs_info(steam_id)

        if json_object:
            total_kills = json_object[0]["value"]

            if weapon == "pistol":
                kills_pistol = json_object[11]["value"]  # glock
                kills_pistol = json_object[135]["value"]  # usp/p2000
                kills_pistol += json_object[139]["value"]  # p250
                kills_pistol += json_object[168]["value"]  # tec
                kills_pistol += json_object[14]["value"]  # five7
                kills_pistol += json_object[13]["value"]  # dual berettas
                #  kills_pistol += json_object[4]["value"]  # CZ
                # kills_pistol += json_object[4]["value"]  # R8
                return (total_kills / kills_pistol) * 100

            elif weapon == "shotgun":
                kills_shotgun = json_object[157]["value"]  # nova
                kills_shotgun += json_object[15]["value"]  # XM
                kills_shotgun += json_object[173]["value"]  # mag-7
                kills_shotgun += json_object[163]["value"]  # sawed

                return (total_kills / kills_shotgun) * 100

            elif weapon == "sniper":
                kills_sniper = json_object[19]["value"]  # awp
                kills_sniper += json_object[149]["value"]  # matapatos
                kills_sniper += json_object[12]["value"]  # deagle

                return (total_kills / kills_sniper) * 100

            elif weapon == "rifles":
                kills_rifle = json_object[20]["value"]  # AK-47
                kills_rifle += json_object[176]["value"]  # M4
                kills_rifle += json_object[22]["value"]  # FAMAS
                kills_rifle += json_object[177]["value"]  # GALIL

                return (total_kills / kills_rifle) * 100

            elif weapon == "smg":
                kills_smg = json_object[152]["value"]  # mp7
                kills_smg += json_object[153]["value"]  # mp9
                kills_smg += json_object[16]["value"]  # MAC-10
                kills_smg += json_object[17]["value"]  # ump
                kills_smg += json_object[167]["value"]  # bizon

                return (total_kills / kills_smg) * 100

            elif weapon == "knife":

                return json_object[9]["value"]

            else:
                kills_throwable = json_object[10]["value"]  # HE
                kills_throwable += json_object[178]["value"]  # molotov

                return (total_kills / kills_throwable) * 100
        else:
            return None
"""
