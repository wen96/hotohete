import urllib2
import json


class SteamAPIService(object):
    @classmethod
    def get_steam_id_from_nick_name(cls, nickname):
        api_key = ""
        url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
        url_params = "?key={}&vanityurl={}".format(api_key, nickname)
        response = urllib2.urlopen("{}{}".format(url, url_params))
        response_content = response.read()
        json_object = json.loads(response_content)
        steam_id = json_object["response"]["steamid"]
        return steam_id

    @classmethod
    def get_steam_info(cls, nickname):
        api_key = ""
        url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
        url_params = "?key={}&steamids={}".format(api_key, cls.get_steam_id_from_nick_name(nickname))
        response = urllib2.urlopen("{}{}".format(url, url_params))
        response_content = response.read()
        json_object = json.loads(response_content)
        return json_object["response"]["players"][0]

    @classmethod
    def get_cs_info(cls, nickname):
        api_key = ""
        url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"
        url_params = "?appid=730&key={}&steamid={}".format(api_key, cls.get_steam_id_from_nick_name(nickname))
        response = urllib2.urlopen("{}{}".format(url, url_params))
        response_content = response.read()
        json_object = json.loads(response_content)
        return json_object["playerstats"]["stats"]
