# -*- coding utf-8 -*-
from unittest import TestCase
from mock import Mock

from api.services.csuser_stats_service import CSUserStatsService
from api.models.csuser import CSUser


class CSUserStatsServiceTesCase(TestCase):
    def test_category_weapons_return_empty_dic_if_csgo_info_is_none(self):
        # Arrange
        csgo_info = None

        #  Act
        result = CSUserStatsService.calculate_category_weapons_kills(csgo_info)

        # Assert
        self.assertEqual(result, {})

    def test_category_weapons_return_weapon_kills(self):
        # Arrange
        csgo_info = {
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
        result = CSUserStatsService.calculate_category_weapons_kills(csgo_info)

        # Assert
        self.assertEqual(result['smg'], 50)
        self.assertEqual(result['sniper'], 20)
        self.assertEqual(result['pistol'], 60)
        self.assertEqual(result['rifle'], 40)
        self.assertEqual(result['shotgun'], 40)
        self.assertEqual(result['throw'], 20)
        self.assertEqual(result['other'], (900 - 230))
        self.assertEqual(len(result.keys()), 7)

    def test_users_by_hours_max_hours_returns_users_sorted(self):
        player1 = Mock(spec=CSUser, csgo_info={'total_time_played': 1})
        player2 = Mock(spec=CSUser, csgo_info={'total_time_played': 2})
        player3 = Mock(spec=CSUser, csgo_info={'total_time_played': 3})
        users = [player3, player1, player2]

        result = CSUserStatsService.users_by_hours_max_hours(users)

        self.assertEqual(result[0], player3)
        self.assertEqual(result[1], player2)
        self.assertEqual(result[2], player1)

    def test_users_by_hours_max_hours_when_empty_user_list(self):
        users = []

        result = CSUserStatsService.users_by_hours_max_hours(users)

        self.assertEqual(result, [])

    def test_users_by_hours_max_hours_when_hours_info(self):
        users = [Mock(spec=CSUser, csgo_info={'total_time_played': 1}), Mock(spec=CSUser, csgo_info={})]

        result = CSUserStatsService.users_by_hours_max_hours(users)

        self.assertEqual(result, users)
