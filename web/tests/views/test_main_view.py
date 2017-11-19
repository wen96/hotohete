import mock

from django.test import TestCase
from api.models import CSTeam, CSUser


class MainViewTest(TestCase):
    def testing_main_view_return_404(self):
        response = self.client.get('BOCADILLO')

        self.assertEqual(response.status_code, 404)

    @mock.patch('api.services.steam_api_service.SteamAPIService.get_steam_id_from_nick_name')
    @mock.patch('api.services.steam_api_service.SteamAPIService.get_steam_info')
    @mock.patch('api.services.steam_api_service.SteamAPIService.get_cs_info')
    def testing_main_view_list_teams(self, mock_cs_info, mock_steam_info, mock_steam_id):
        mock_cs_info.return_value = {}
        mock_steam_info.return_value = {}
        mock_steam_id.return_value = '1234'
        CSTeam.objects.create(name='sandwich')
        CSUser.objects.create(steam_username='testuser')
        CSTeam.objects.create(name='lamers')

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['teams']), list(CSTeam.objects.all()))
