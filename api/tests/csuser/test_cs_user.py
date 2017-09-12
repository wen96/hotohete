# -*- coding utf-8 -*-
from unittest import TestCase

import mock

from api.models.csuser import CSUser
from api.services.steam_api_service import SteamAPIService


class CSUserTesCase(TestCase):

    def test__str__returns_username(self):
        #  Act
        user_for_test = CSUser(steam_username='Pepe')

        # Assert
        self.assertEqual(str(user_for_test), user_for_test.steam_username)

    def test_user_get_steam_id_returns_steam_id_when_exists(self):
        # Arrange
        user_for_test = CSUser()
        user_for_test.steam_id = '123'

        #  Act
        result = user_for_test.get_steam_id

        # Assert
        self.assertEqual(result, '123')

    @mock.patch.object(SteamAPIService, 'get_steam_id_from_nick_name')
    def test_user_get_steam_id_calls_steam_api_when_id_property_does_not_exist(
            self, mock_get_steam_id_from_nick_name, ):
        # Arrange
        mock_get_steam_id_from_nick_name.return_value = 'id'
        user_for_test = CSUser()

        #  Act
        result = user_for_test.get_steam_id

        # Assert
        self.assertEqual(result, 'id')

    @mock.patch.object(SteamAPIService, 'get_steam_info')
    @mock.patch.object(CSUser, 'get_steam_id', new_callable=mock.PropertyMock)
    def test_steam_info_call_steam_info_and_steam_id_returning_steam_info_result(
            self, mock_get_steam_id, mock_get_steam_info):
        # Arrange
        mock_get_steam_info.return_value = 'steam_info'
        mock_get_steam_id.return_value = 'Javier'
        user_for_test = CSUser()

        #  Act
        result = user_for_test.steam_info

        # Assert
        self.assertEqual(result, 'steam_info')
        self.assertEqual(mock_get_steam_id.call_count, 2)
        self.assertEqual(mock_get_steam_info.call_count, 1)
        self.assertEqual(mock_get_steam_info.call_args, mock.call('Javier'))

    @mock.patch.object(CSUser, 'get_steam_id', new_callable=mock.PropertyMock)
    def test_steam_info_returns_none_if_not_steam_id(self, mock_get_steam_id):
        # Arrange
        mock_get_steam_id.return_value = None
        user_for_test = CSUser()

        #  Act
        result = user_for_test.steam_info

        # Assert
        self.assertIsNone(result)
        self.assertEqual(mock_get_steam_id.call_count, 1)

    @mock.patch.object(CSUser, 'get_steam_id', new_callable=mock.PropertyMock)
    def test_csgo_info_returns_none_if_not_steam_id(self, mock_get_steam_id):
        # Arrange
        mock_get_steam_id.return_value = None
        user_for_test = CSUser()

        #  Act
        result = user_for_test.csgo_info

        # Assert
        self.assertIsNone(result)
        self.assertEqual(mock_get_steam_id.call_count, 1)

    @mock.patch.object(SteamAPIService, 'get_cs_info')
    @mock.patch.object(CSUser, 'get_steam_id', new_callable=mock.PropertyMock)
    def test_csgo_info_return_empty_dict_when_service_returns_none(self, mock_get_steam_id, mock_get_cs_info):
        # Arrange
        mock_get_cs_info.return_value = None
        mock_get_steam_id.return_value = 'Javier'
        user_for_test = CSUser()

        #  Act
        result = user_for_test.csgo_info

        # Assert
        self.assertEqual(result, {})
        self.assertEqual(mock_get_steam_id.call_count, 2)
        self.assertEqual(mock_get_cs_info.call_count, 1)
        self.assertEqual(mock_get_cs_info.call_args, mock.call('Javier'))

    @mock.patch.object(SteamAPIService, 'get_cs_info')
    @mock.patch.object(CSUser, 'get_steam_id', new_callable=mock.PropertyMock)
    def test_csgo_info_transforms_array_response_to_dict(self, mock_get_steam_id, mock_get_cs_info):
        # Arrange
        mock_get_cs_info.return_value = [{"name": "total_kills_p90", "value": 20}]
        mock_get_steam_id.return_value = 'Javier'
        user_for_test = CSUser()

        #  Act
        result = user_for_test.csgo_info

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result['total_kills_p90'], 20)

    @mock.patch.object(CSUser, 'csgo_info', new_callable=mock.PropertyMock)
    def test_category_weapons_return_empty_dic_if_csgo_info_is_none(self, mock_csgo_info):
        # Arrange
        user_for_test = CSUser()
        mock_csgo_info.return_value = None

        #  Act
        result = user_for_test.category_weapons_kills

        # Assert
        self.assertEqual(result, {})

    @mock.patch.object(CSUser, 'csgo_info', new_callable=mock.PropertyMock)
    def test_category_weapons_return_weapon_kills(self, mock_csgo_info):
        # Arrange
        user_for_test = CSUser()
        mock_csgo_info.return_value = {
            'total_kills_p90': 10,
            'total_kills_bizon': 10,
            'total_kills_ump45': 10,
            'total_kills_mp7': 10,
            'total_kills_mp9': 10,
            'total_kills_awp': 10,
            'total_kills_ssg08': 10,
            'total_kills_glock': 10,
            'total_kills_deagle': 10,
            'total_kills_elite': 10,
            'total_kills_fiveseven': 10,
            'total_kills_hkp2000': 10,
            'total_kills_p250': 10,
            'total_kills_ak47': 10,
            'total_kills_m4a1': 10,
            'total_kills_famas': 10,
            'total_kills_galilar': 10,
            'total_kills_mag7': 10,
            'total_kills_xm1014': 10,
            'total_kills_nova': 10,
            'total_kills_sawedoff': 10,
            'total_kills_hegrenade': 10,
            'total_kills_molotov': 10,
            'total_kills': 900}

        #  Act
        result = user_for_test.category_weapons_kills

        # Assert
        self.assertEqual(result['smg'], 50)
        self.assertEqual(result['sniper'], 20)
        self.assertEqual(result['pistol'], 60)
        self.assertEqual(result['rifle'], 40)
        self.assertEqual(result['shotgun'], 40)
        self.assertEqual(result['throw'], 20)
        self.assertEqual(result['other'], (900 - 230))
        self.assertEqual(len(result.keys()), 7)
