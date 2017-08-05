from django.test import Client
from django.test import TestCase


class MainViewTest(TestCase):

    def testing_main_view_return_200(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(200, response.status_code)

    def testing_main_view_return_404(self):
        c = Client()
        response = c.get('BOCADILLO')
        self.assertEqual(404, response.status_code)
