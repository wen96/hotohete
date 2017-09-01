from django.test import TestCase
from api.models import CSTeam


class MainViewTest(TestCase):
    def testing_main_view_return_404(self):
        response = self.client.get('BOCADILLO')

        self.assertEqual(response.status_code, 404)

    def testing_main_view_list_teams(self):
        CSTeam.objects.create(name='sandwich')
        CSTeam.objects.create(name='lamers')

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['teams']), list(CSTeam.objects.all()))
