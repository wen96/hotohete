import mock
import urllib2

from django.test import TestCase
from api.services import SteamAPIService


class SteamApiServiceTestCase(TestCase):

    def test_api_key_returned_when_exist(self):
        # Act
        service = SteamAPIService()
        service._api_key = 'holita'

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

        # Act
        service = SteamAPIService()
        result = service.get_steam_id_from_nick_name(nickname)

        # Asssert
        self.assertIsNone(result)

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_get_steam_id_from_nick_name_returns_steam_id(self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_api_key.return_value = 'hummus'
        mock_request_endpoint.return_value = {'response': {'steamid': '12341234'}}
        nickname = 'clapton'

        # Act
        service = SteamAPIService()
        result = service.get_steam_id_from_nick_name(nickname)

        # Asssert
        self.assertEqual(result, '12341234')

    def test__init__default_var(self):
        #  Act
        service = SteamAPIService()

        #  Assert
        self.assertIsNone(service._api_key)  # pylint: disable=protected-access
        self.assertEqual(service.cache_steam_info, {})
        self.assertEqual(service.base_url, 'http://api.steampowered.com')

    def test_cs_info_returns_none_if_steam_id_is_none(self):
        #  Act
        steam_id = None
        service = SteamAPIService()
        result = service.get_cs_info(steam_id)

        #  Assert
        self.assertIsNone(result)

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_cs_info_returns_none_cause_playerstats_not_found(self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_request_endpoint.return_value = False
        steam_id = 1234

        #  Act
        service = SteamAPIService()
        result = service.get_cs_info(steam_id)

        # Assert
        self.assertIsNone(result)

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_cs_info_returns_playerstats(self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_request_endpoint.return_value = {'playerstats': {'stats': 'statA'}}
        steam_id = 1234

        #  Act
        service = SteamAPIService()
        result = service.get_cs_info(steam_id)

        # Assert
        self.assertEqual(result, 'statA')

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_cs_info_urls_properly_formed(self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_api_key.return_value = 'hummus'
        steam_id = 1234
        url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"
        url_params = "?appid=730&key=hummus&steamid=1234"
        super_url = "{}{}".format(url, url_params)

        #  Act
        service = SteamAPIService()
        service.get_cs_info(steam_id)

        # Assert
        mock_request_endpoint.assert_called_with(super_url)

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_get_steam_info_urls_properly_formed(self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_api_key.return_value = 'hummus'
        steam_id = 1234
        url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
        url_params = "?key=hummus&steamids=1234"
        super_url = "{}{}".format(url, url_params)

        #  Act
        service = SteamAPIService()
        service.get_steam_info(steam_id)

        # Assert
        mock_request_endpoint.assert_called_with(super_url)

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key', new_callable=mock.PropertyMock)
    def test_get_steam_info_set_steam_id_cache_as_none_cause_cs_profile_not_founded(
            self, mock_api_key, mock_request_endpoint):

        # Arrange
        mock_request_endpoint.return_value = None
        mock_api_key.return_value = 'hummus'
        steam_id = 1234
        #  Act
        service = SteamAPIService()
        service.get_steam_info(steam_id)

        # Assert
        self.assertIsNone(service.cache_steam_info[steam_id])

    @mock.patch.object(urllib2, 'urlopen')
    def test_request_service_returns_none_if_fails_to_request(self, urllib_open):
        # Arrange
        urllib_open.side_effect = urllib2.HTTPError('', 500, '', None, None)
        url = 'urltonothing'
        service = SteamAPIService()

        #  Act
        result = service._request_endpoint(url)

        # Assert
        self.assertIsNone(result)

    @mock.patch.object(urllib2, 'urlopen')
    def test_request_service_returns_json_object_deserialized_from_response(self, urllib_open):
        # Arrange
        urllib_open.return_value.read.return_value = '{}'
        url = 'urltonothing'
        service = SteamAPIService()

        #  Act
        result = service._request_endpoint(url)

        # Assert
        self.assertEqual(result, {})
