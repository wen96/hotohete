# -*- coding utf-8 -*-
import mock

from django.test import TestCase
from api.models.csuser import CSUser
from api.services import SteamAPIService


class CsUserFunctionsTesCase(TestCase):

    def test__str__returns_username(self):
        #  Act
        user_for_test = CSUser()
        user_for_test.steam_username = 'Pepe'

        # Assert
        self.assertEqual(str(user_for_test), user_for_test.steam_username)

    def test_CSUser_init_csgo_as_none(self):
        #  Act
        user_for_test = CSUser()
        # Assert
        self.assertIsNone(user_for_test.csgo_info)

    def test_user_get_steam_id_returns_steam_id_when_exists(self):
        #  Act
        user_for_test = CSUser()
        user_for_test.steam_id = '123'
        result = user_for_test.get_steam_id
        # Assert
        self.assertEqual(result, '123')

    @mock.patch.object(SteamAPIService, 'get_steam_id_from_nick_name')
    def test_user_get_steam_id_returns_steam_id_when_does_not_exist(self, mock_get_steam_id_from_nick_name, ):
        # Arrange
        mock_get_steam_id_from_nick_name.return_value = 'id'

        #  Act
        user_for_test = CSUser()
        result = user_for_test.get_steam_id

        # Assert
        self.assertEqual(result, 'id')

    @mock.patch.object(SteamAPIService, 'get_steam_info')
    @mock.patch.object(CSUser, 'get_steam_id', new_callable=mock.PropertyMock)
    def test_get_steam_info(self, mock_get_steam_id, mock_get_steam_info):
        # Arrange

        mock_get_steam_info.return_value = 'steam_info'
        mock_get_steam_id.return_value = 'Javier'
        #  Act
        user_for_test = CSUser()

        result = user_for_test.get_steam_info

        # Assert
        self.assertEqual(result, 'steam_info')

    def test_cs_info_is_returned_when_exists(self):
        #  Act
        user_for_test = CSUser()
        user_for_test.csgo_info = 'cs_info'
        result = user_for_test.get_cs_info

        # Assert
        self.assertEqual(result, 'cs_info')

    @mock.patch.object(SteamAPIService, 'get_cs_info')
    @mock.patch.object(CSUser, 'get_steam_id', new_callable=mock.PropertyMock)
    def test_cs_info_return_empty_dic_when_get_cs_info_return_none(self, mock_get_steam_id, mock_get_cs_info):
        # Arrange

        mock_get_cs_info.return_value = []
        mock_get_steam_id.return_value = 'Javier'

        #  Act
        user_for_test = CSUser()
        result = user_for_test.get_cs_info

        # Assert
        self.assertEqual(result, {})
