import urllib2
import json
from api.models.hotohete_settings import HotoheteSettings


class SteamAPIService(object):

    def __init__(self):
        self._api_key = None
        self.base_url = 'http://api.steampowered.com'
        self.cache_steam_info = {}
        self.cache_csgo_info = {}

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
        if steam_id and steam_id not in self.cache_csgo_info:

            url = "{}/ISteamUserStats/GetUserStatsForGame/v0002/".format(self.base_url)
            url_params = "?appid=730&key={}&steamid={}".format(self.api_key, steam_id)

            json_object = self._request_endpoint("{}{}".format(url, url_params))

            self.cache_csgo_info[steam_id] = json_object["playerstats"]["stats"] if json_object else None

        return self.cache_csgo_info[steam_id]

    def _request_endpoint(self, url):
        """ Returns an object loaded from a response expecting json response. None if 500 error.
        """
        try:
            response = urllib2.urlopen(url)
            return json.loads(response.read())
        except urllib2.HTTPError:

            return None
