from django.views.generic import View
from django.shortcuts import render

from api.models import CSTeam


class MainView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        teams = CSTeam.objects.all()
        return render(request, self.template_name, {
            'teams': teams
        })
