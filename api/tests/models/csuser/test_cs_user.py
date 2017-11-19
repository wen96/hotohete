# -*- coding utf-8 -*-
from unittest import TestCase

import mock

from api.models.csuser import CSUser
from api.services.steam_api_service import SteamAPIService
from api.services.csuser_stats_service import CSUserStatsService


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

    @mock.patch.object(CSUserStatsService, 'calculate_category_weapons_kills')
    @mock.patch.object(CSUser, 'csgo_info', new_callable=mock.PropertyMock)
    def test_category_weapons_calls_service_calculate_stats_for_weapon(self, mock_csgo_info, mock_stats_calculate):
        # Arrange
        mock_stats_calculate.return_value = {'stats': 'happy'}
        mock_csgo_info.return_value = {'csgo': 'info'}
        user_for_test = CSUser()

        #  Act
        result = user_for_test.category_weapons_kills

        # Assert
        self.assertEqual(result, {'stats': 'happy'})
        self.assertEqual(mock_csgo_info.call_count, 1)
        self.assertEqual(mock_stats_calculate.call_count, 1)
        self.assertEqual(mock_stats_calculate.call_args, mock.call({'csgo': 'info'}))

    @mock.patch.object(CSUserStatsService, 'calculate_maps_stats')
    @mock.patch.object(CSUser, 'csgo_info', new_callable=mock.PropertyMock)
    def test_maps_stats_calls_calculation_service(self, mock_csgo_info, mock_stats_calculate):
        # Arrange
        mock_stats_calculate.return_value = {'stats': 'happy'}
        mock_csgo_info.return_value = {'csgo': 'info'}
        user_for_test = CSUser()

        #  Act
        result = user_for_test.maps_stats

        # Assert
        self.assertEqual(result, {'stats': 'happy'})
        self.assertEqual(mock_csgo_info.call_count, 1)
        self.assertEqual(mock_stats_calculate.call_count, 1)
        self.assertEqual(mock_stats_calculate.call_args, mock.call({'csgo': 'info'}))
