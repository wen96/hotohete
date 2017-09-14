from unittest import TestCase

import urllib2
import mock

from api.services.steam_api_service import SteamAPIService


class SteamApiServiceTestCase(TestCase):

    def test_api_key_returned_when_exist(self):
        # Arrange
        service = SteamAPIService()

        # Act
        service._api_key = 'holita'  # pylint: disable=protected-access

        # Asssert
        self.assertEqual(service.api_key, 'holita')

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_get_steam_id_from_nick_name_returns_none_if_user_not_found_in_reponse(
            self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_api_key.return_value = 'hummus'
        mock_request_endpoint.return_value = {'response': {'error': 'asdf'}}
        nickname = 'clapton'
        url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={}&vanityurl={}'.format(
            mock_api_key.return_value, nickname)
        service = SteamAPIService()

        # Act
        result = service.get_steam_id_from_nick_name(nickname)

        # Asssert
        self.assertIsNone(result)
        self.assertEqual(mock_api_key.call_count, 1)
        self.assertEqual(mock_request_endpoint.call_count, 1)
        self.assertEqual(mock_request_endpoint.call_args, mock.call(url))

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_get_steam_id_from_nick_name_returns_steam_id(self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_api_key.return_value = 'hummus'
        mock_request_endpoint.return_value = {'response': {'steamid': '12341234'}}
        nickname = 'clapton'
        url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={}&vanityurl={}'.format(
            mock_api_key.return_value, nickname)
        service = SteamAPIService()

        # Act
        result = service.get_steam_id_from_nick_name(nickname)
        self.assertEqual(mock_request_endpoint.call_count, 1)

        # Asssert
        self.assertEqual(result, '12341234')
        self.assertEqual(mock_api_key.call_count, 1)
        self.assertEqual(mock_request_endpoint.call_count, 1)
        self.assertEqual(mock_request_endpoint.call_args, mock.call(url))

    def test__init__default_var(self):
        #  Act
        service = SteamAPIService()

        #  Assert
        self.assertIsNone(service._api_key)  # pylint: disable=protected-access
        self.assertEqual(service.cache_steam_info, {})
        self.assertEqual(service.base_url, 'http://api.steampowered.com')

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_cs_info_returns_none_cause_playerstats_not_found(self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_request_endpoint.return_value = None
        steam_id = 1234
        mock_api_key.return_value = 'hummus'
        url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"
        url_params = "?appid=730&key=hummus&steamid=1234"
        super_url = "{}{}".format(url, url_params)
        service = SteamAPIService()

        #  Act
        result = service.get_cs_info(steam_id)

        # Assert
        self.assertIsNone(result)
        self.assertEqual(mock_request_endpoint.call_count, 1)
        self.assertEqual(mock_request_endpoint.call_args, mock.call(super_url))

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_cs_info_returns_playerstats(self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_request_endpoint.return_value = {'playerstats': {'stats': 'statA'}}
        steam_id = 1234
        mock_api_key.return_value = 'hummus'
        url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"
        url_params = "?appid=730&key=hummus&steamid=1234"
        super_url = "{}{}".format(url, url_params)
        service = SteamAPIService()

        #  Act
        result = service.get_cs_info(steam_id)

        # Assert
        self.assertEqual(result, 'statA')
        self.assertEqual(mock_request_endpoint.call_count, 1)
        self.assertEqual(mock_request_endpoint.call_args, mock.call(super_url))

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_cs_info_urls_properly_formed(self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_api_key.return_value = 'hummus'
        steam_id = 1234
        url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"
        url_params = "?appid=730&key=hummus&steamid=1234"
        super_url = "{}{}".format(url, url_params)
        service = SteamAPIService()

        #  Act
        service.get_cs_info(steam_id)

        # Assert
        mock_request_endpoint.assert_called_with(super_url)
        self.assertEqual(mock_request_endpoint.call_count, 1)
        self.assertEqual(mock_request_endpoint.call_args, mock.call(super_url))

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_get_steam_info_urls_properly_formed(self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_api_key.return_value = 'hummus'
        steam_id = 1234
        url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
        url_params = "?key=hummus&steamids=1234"
        super_url = "{}{}".format(url, url_params)
        service = SteamAPIService()

        #  Act
        service.get_steam_info(steam_id)

        # Assert
        mock_request_endpoint.assert_called_with(super_url)
        self.assertEqual(mock_request_endpoint.call_count, 1)
        self.assertEqual(mock_request_endpoint.call_args, mock.call(super_url))

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_get_steam_info_set_steam_id_cache_as_none_cause_cs_profile_not_found(
            self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_request_endpoint.return_value = None
        mock_api_key.return_value = 'hummus'
        steam_id = 1234
        url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
        url_params = "?key=hummus&steamids=1234"
        super_url = "{}{}".format(url, url_params)
        service = SteamAPIService()

        #  Act
        service.get_steam_info(steam_id)

        # Assert
        self.assertIsNone(service.cache_steam_info[steam_id])
        self.assertEqual(mock_request_endpoint.call_count, 1)
        self.assertEqual(mock_request_endpoint.call_args, mock.call(super_url))

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_get_steam_info_when_called_twice_returns_cache_value(self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_api_key.return_value = 'hummus'
        steam_id = 1234
        url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
        url_params = "?key=hummus&steamids=1234"
        super_url = "{}{}".format(url, url_params)
        service = SteamAPIService()

        #  Act
        service.get_steam_info(steam_id)
        service.get_steam_info(steam_id)

        # Assert
        self.assertEqual(mock_request_endpoint.call_count, 1)
        mock_request_endpoint.assert_called_with(super_url)

    @mock.patch.object(urllib2, 'urlopen')
    def test_request_service_returns_none_if_fails_to_request(self, urllib_open):
        # Arrange
        urllib_open.side_effect = urllib2.HTTPError('', 500, '', None, None)
        url = 'urltonothing'
        service = SteamAPIService()

        #  Act
        result = service._request_endpoint(url)  # pylint: disable=protected-access

        # Assert
        self.assertIsNone(result)

    @mock.patch.object(urllib2, 'urlopen')
    def test_request_service_returns_json_object_deserialized_from_response(self, urllib_open):
        # Arrange
        urllib_open.return_value.read.return_value = '{}'
        url = 'urltonothing'
        service = SteamAPIService()

        #  Act
        result = service._request_endpoint(url)  # pylint: disable=protected-access

        # Assert
        self.assertEqual(result, {})
