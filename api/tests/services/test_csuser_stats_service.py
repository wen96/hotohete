# -*- coding utf-8 -*-
from unittest import TestCase
from mock import Mock

from api.services.csuser_stats_service import CSUserStatsService
from api.models.csuser import CSUser
from api.tests.services.csgo_info_fixtures import create_csgo_info


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

    def test_maps_stats_from_user(self):
        # Arrange
        csgo_info = create_csgo_info()

        #  Act
        result = CSUserStatsService.calculate_maps_stats(csgo_info)

        # Assert
        self.assertEqual(len(result), 21)
        self.assertEqual(result['ar_monastery'], {'wins': 18, 'lost': 20, 'played': 38})
        self.assertEqual(result['de_sugarcane'], {'wins': 11, 'lost': 14, 'played': 25})
        self.assertEqual(result['de_dust2'], {'wins': 758, 'lost': 875, 'played': 1633})
        self.assertEqual(result['de_stmarc'], {'wins': 89, 'lost': 97, 'played': 186})
        self.assertEqual(result['de_bank'], {'wins': 70, 'lost': 117, 'played': 187})
        self.assertEqual(result['cs_assault'], {'wins': 0, 'lost': 7, 'played': 7})
        self.assertEqual(result['ar_baggage'], {'wins': 31, 'lost': 23, 'played': 54})
        self.assertEqual(result['de_train'], {'wins': 168, 'lost': 185, 'played': 353})
        self.assertEqual(result['de_cbble'], {'wins': 450, 'lost': 517, 'played': 967})
        self.assertEqual(result['de_dust'], {'wins': 2, 'lost': 0, 'played': 2})
        self.assertEqual(result['de_shorttrain'], {'wins': 130, 'lost': 140, 'played': 270})
        self.assertEqual(result['cs_office'], {'wins': 19, 'lost': 28, 'played': 47})
        self.assertEqual(result['cs_italy'], {'wins': 1, 'lost': 0, 'played': 1})
        self.assertEqual(result['de_nuke'], {'wins': 27, 'lost': 26, 'played': 53})
        self.assertEqual(result['de_aztec'], {'wins': 0, 'lost': 2, 'played': 2})
        self.assertEqual(result['de_house'], {'wins': 5, 'lost': 0, 'played': 5})
        self.assertEqual(result['de_safehouse'], {'wins': 245, 'lost': 244, 'played': 489})
        self.assertEqual(result['de_lake'], {'wins': 246, 'lost': 274, 'played': 520})
        self.assertEqual(result['de_inferno'], {'wins': 2169, 'lost': 2226, 'played': 4395})
        self.assertEqual(result['ar_shoots'], {'wins': 105, 'lost': 104, 'played': 209})
        self.assertEqual(result['unknown'], {'wins': 5752, 'lost': 6020, 'played': 11772})

    def test_weapon_stats_from_user(self):
        # Arrange
        csgo_info = create_csgo_info()

        #  Act
        result = CSUserStatsService.calculate_weapon_stats(csgo_info)

        # Assert
        self.assertEqual(len(result), 30)
        self.assertEqual(result['famas'], {'hits': 3467, 'ratio': 0.24720142602495543, 'shots': 14025})
        self.assertEqual(result['ak47'], {'hits': 18189, 'ratio': 0.19485152333204783, 'shots': 93348})
        self.assertEqual(result['m4a1'], {'hits': 28073, 'ratio': 0.22089244545161266, 'shots': 127089})

    def test_calculate_user_elo(self):
        # Arrange
        csgo_info = create_csgo_info()

        # Act
        result = CSUserStatsService.calculate_elo(csgo_info)

        # Assert
        self.assertEqual(result, 36.38547410602409)

    def test_calculate_user_by_elo(self):
        # Arrange
        best_player = Mock(csgo_info=create_csgo_info())
        best_player.csgo_info['total_kills'] += 100
        worst_player = Mock(csgo_info=create_csgo_info())
        worst_player.csgo_info['total_kills'] -= 100
        middle_player = Mock(csgo_info=create_csgo_info())
        users = [best_player, worst_player, middle_player]

        # Act
        result = CSUserStatsService.users_by_elo(users)

        # Assert
        self.assertEqual(result, [best_player, middle_player, worst_player])

    def test_calculate_kill_death_ration_no_csgo_info(self):
        # Arrang
        csgo_info = None

        # Act
        result = CSUserStatsService.calculate_kill_death_ratio(csgo_info)

        # Assert
        self.assertEqual(result, 0.0)
