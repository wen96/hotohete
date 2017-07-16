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
        url = "{}/ISteamUser/ResolveVanityURL/v0001/".format(self.base_url)
        url_params = "?key={}&vanityurl={}".format(self.api_key, nickname)
        response = urllib2.urlopen("{}{}".format(url, url_params))
        response_content = response.read()
        json_object = json.loads(response_content)
        return json_object["response"]["steamid"]

    def get_steam_info(self, steam_id):
        # TODO: Use a cache with TTL (time to live)
        if steam_id not in self.cache_steam_info:
            url = "{}/ISteamUser/GetPlayerSummaries/v0002/".format(self.base_url)
            url_params = "?key={}&steamids={}".format(self.api_key, steam_id)
            response = urllib2.urlopen("{}{}".format(url, url_params))
            response_content = response.read()
            json_object = json.loads(response_content)
            self.cache_steam_info[steam_id] = json_object["response"]["players"][0]
        return self.cache_steam_info[steam_id]

    def get_cs_info(self, steam_id):
        url = "{}/ISteamUserStats/GetUserStatsForGame/v0002/".format(self.base_url)
        url_params = "?appid=730&key={}&steamid={}".format(self.api_key, steam_id)
        response = urllib2.urlopen("{}{}".format(url, url_params))
        response_content = response.read()
        json_object = json.loads(response_content)
        return json_object["playerstats"]["stats"]
