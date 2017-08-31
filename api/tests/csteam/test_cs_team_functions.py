from unittest import TestCase
from api.models.csteam import CSTeam


class CsTeamFunctionsTesCase(TestCase):

    def test__str__returns_username(self):
        #  Act
        team_for_test = CSTeam(name='cerosesenta')

        # Assert
        self.assertEqual(str(team_for_test), team_for_test.name)
