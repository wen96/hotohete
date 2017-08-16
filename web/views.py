from django.views.generic import View
from django.shortcuts import render, get_object_or_404

from api.models import CSTeam


class MainView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        teams = CSTeam.objects.all()
        return render(request, self.template_name, {
            'teams': teams
        })


class TeamDetailView(View):
    template_name = 'team_detail.html'

    def get(self, request, team_id, *args, **kwargs):
        team = get_object_or_404(CSTeam, pk=team_id)
        return render(request, self.template_name, {
            'team': team
        })
