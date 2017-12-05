# -*- coding utf-8 -*-
from unittest import TestCase
from mock import Mock

from api.services.overall_stats_service import OverallStatsService
from api.services.csuser_stats_service import CSUserStatsService
from api.models.csuser import CSUser
from api.tests.services.csgo_info_fixtures import create_csgo_info


class OverallStatsServiceTesCase(TestCase):
    def test_calculate_map_stats(self):
        # Arrange
        map_stats = CSUserStatsService.calculate_maps_stats(create_csgo_info())
        users = [Mock(spec=CSUser, maps_stats=map_stats), Mock(spec=CSUser, maps_stats=map_stats)]

        #  Act
        result = OverallStatsService.maps_stats_from_users(users)

        # Assert
        self.assertEqual(len(result), 21)
        self.assertEqual(result['de_train'], {'wins': 168 * 2, 'lost': 185 * 2, 'played': 353 * 2})

    def test_calculate_weapon_stats(self):
        # Arrange
        weapon_stats = CSUserStatsService.calculate_weapon_stats(create_csgo_info())
        users = [Mock(spec=CSUser, weapon_stats=weapon_stats), Mock(spec=CSUser, weapon_stats=weapon_stats)]

        #  Act
        result = OverallStatsService.weapon_stats_from_users(users)

        # Assert
        self.assertEqual(len(result), 30)
        self.assertEqual(result['famas'], {'hits': 3467 * 2, 'shots': 14025 * 2})
        self.assertEqual(result['ak47'], {'hits': 18189 * 2, 'shots': 93348 * 2})
        self.assertEqual(result['m4a1'], {'hits': 28073 * 2, 'shots': 127089 * 2})

    def test_sort_maps_stats(self):
        # Arrange
        map_stats = CSUserStatsService.calculate_maps_stats(create_csgo_info())
        users = [Mock(spec=CSUser, maps_stats=map_stats), Mock(spec=CSUser, maps_stats=map_stats)]
        map_stats = OverallStatsService.maps_stats_from_users(users)

        #  Act
        result = OverallStatsService.maps_by_played(map_stats)

        # Assert
        self.assertEqual(len(result), 21)
        self.assertEqual(result[0]['name'], 'unknown')
        self.assertEqual(result[1]['name'], 'de_inferno')
        self.assertEqual(result[2]['name'], 'de_dust2')
        self.assertEqual(result[3]['name'], 'de_cbble')
