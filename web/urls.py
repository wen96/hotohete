from django.conf.urls import url
from web.views import MainView


urlpatterns = [
    url(r'^', view=MainView.as_view(), name='main_view'),
]
