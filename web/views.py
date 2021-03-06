import json

from django.views.generic import View
from django.shortcuts import render, get_object_or_404

from api.models import CSTeam, CSUser
from api.services.csuser_stats_service import CSUserStatsService
from api.services.overall_stats_service import OverallStatsService


class MainView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        teams = CSTeam.objects.all()
        users = CSUser.objects.filter(visible=True)
        users_by_elo = CSUserStatsService.users_by_elo(users)
        return render(request, self.template_name, {
            'teams': teams,
            'users_by_hours': CSUserStatsService.users_by_hours_max_hours(users),
            'users_by_elo': users_by_elo,
            'top_player': users_by_elo[0] if users_by_elo else None,
            'map_stats': json.dumps(OverallStatsService.maps_stats_from_users(users)),
            'weapon_stats': json.dumps(OverallStatsService.weapon_stats_from_users(users)),
        })


class TeamDetailView(View):
    template_name = 'team_detail.html'

    def get(self, request, team_id, *args, **kwargs):
        team = get_object_or_404(CSTeam, pk=team_id)
        return render(request, self.template_name, {
            'team': team
        })


class ELOStatsView(View):
    template_name = 'elo_stats.html'

    def get(self, request, *args, **kwargs):
        users = CSUser.objects.filter(visible=True)
        users_by_elo = CSUserStatsService.users_by_elo(users)
        return render(request, self.template_name, {
            'users_by_elo': users_by_elo
        })
