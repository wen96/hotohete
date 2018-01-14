from django.conf.urls import url
from web.views import MainView, TeamDetailView, ELOStatsView


urlpatterns = [
    url(r'^elo-stats/$', view=ELOStatsView.as_view(), name='elo_stats'),
    url(r'^teams/([0-9])/$', view=TeamDetailView.as_view(), name='team_detail'),
    url(r'^$', view=MainView.as_view(), name='main_view'),
]
