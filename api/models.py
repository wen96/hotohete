# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from api.services import SteamAPIService


class CSTeam(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CSUser(models.Model):
    steam_username = models.CharField(max_length=255)
    team = models.ForeignKey(CSTeam, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.steam_username

    @property
    def get_steam_info(self):
        return SteamAPIService.get_steam_info(self.steam_username)

    @property
    def get_cs_info(self):
        return SteamAPIService.get_cs_info(self.steam_username)
