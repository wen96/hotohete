import mock

from django.test import TestCase
from api.services import SteamAPIService


class SteamApiServiceTestCase(TestCase):

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key')
    def test_get_steam_id_from_nick_name_returns_none_if_user_not_found_in_reponse(self, mock_api_key, mock_request_endpoint):
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
    @mock.patch.object(SteamAPIService, 'api_key')
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
        self.assertIsNone(service._api_key)
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
    @mock.patch.object(SteamAPIService, 'api_key')
    def test_cs_info_returns_none_cause_playerstats_not_found(self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_api_key.return_value = 'hummus'
        mock_request_endpoint.return_value = False
        steam_id = 1234

        #  Act
        service = SteamAPIService()
        result = service.get_cs_info(steam_id)

        # Assert
        self.assertIsNone(result)

    """
    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key')
    def test_cs_info_returns_playerstats(self, mock_api_key, mock_request_endpoint):
        mock_api_key.return_value = 'hummus'
        mock_request_endpoint.return_value = {'playerstats': {'stats'}}
        steam_id = 1234

        #  Act
        service = SteamAPIService()
        result = service.get_cs_info(steam_id)
        self.assertEqual(result, {'playerstats': {'stats'}})
    """
