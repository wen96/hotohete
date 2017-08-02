import mock

from django.test import TestCase
from api.services import SteamAPIService


class SteamApiServiceTestCase(TestCase):

    @mock.patch.object(SteamAPIService, '_request_endpoint')
    @mock.patch.object(SteamAPIService, 'api_key')
    def test_get_steam_id_from_nick_name_returns_none_if_user_not_found_in_reponse(self, mock_api_key, mock_request_endpoint):
        # Arrange
        mock_api_key.return_value = 'morcilla'
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
        mock_api_key.return_value = 'morcilla'
        mock_request_endpoint.return_value = {'response': {'steamid': '12341234'}}
        nickname = 'clapton'

        # Act
        service = SteamAPIService()
        result = service.get_steam_id_from_nick_name(nickname)

        # Asssert
        self.assertEqual(result, '12341234')

    def test_init_api_key_is_none(self):
        service = SteamAPIService()

        self.assertIsNone(service.api_key)

    def test_init_cache_on_creation_is_empty(self):
        service = SteamAPIService()

        self.assertEqual(service.cache_steam_info, {})

    def test_init_base_url_(self):
        service = SteamAPIService()

        self.assertEqual(service.base_url, 'http://api.steampowered.com')
