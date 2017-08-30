from django.test import TestCase
from api.models.csteam import CSTeam


class CsTeamFunctionsTesCase(TestCase):

    def test__str__returns_username(self):
        #  Act
        team_for_test = CSTeam()
        team_for_test.name = 'cerosesenta'

        # Assert
        self.assertEqual(str(team_for_test), team_for_test.name)
