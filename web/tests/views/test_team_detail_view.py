import json
import mock

from django.test import TestCase
from api.models import CSTeam, CSUser, HotoheteSettings


class TeamDetailTest(TestCase):
    @mock.patch('api.services.urllib2')
    def testing_list_team_members(self, mock_urllib2):
        request_union = {
            "response": {"players": {}, "steamid": 1234},
            "playerstats": {"stats": {}}
        }
        mock_urllib2.urlopen.return_value.read.return_value = json.dumps(request_union)
        team = CSTeam.objects.create(name='sandwich')
        CSUser.objects.create(steam_username='fucker', team=team)
        HotoheteSettings.objects.create(key='STEAM_API_KEY', value='MYHAPPYKEY')

        response = self.client.get('/teams/{}/'.format(team.pk))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['team'], team)
        self.assertEqual(mock_urllib2.urlopen.call_count, 3)
        steam_url = 'http://api.steampowered.com/'
        self.assertIn(
            mock.call('{}ISteamUser/ResolveVanityURL/v0001/?key=MYHAPPYKEY&vanityurl=fucker'.format(steam_url)),
            mock_urllib2.urlopen.call_args_list)
        self.assertIn(
            mock.call('{}ISteamUser/GetPlayerSummaries/v0002/?key=MYHAPPYKEY&steamids=1234'.format(steam_url)),
            mock_urllib2.urlopen.call_args_list)
        self.assertIn(
            mock.call('{}ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=MYHAPPYKEY&steamid=1234'.format(
                steam_url)),
            mock_urllib2.urlopen.call_args_list)
