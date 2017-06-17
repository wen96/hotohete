# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class CSTeam(models.Model):
    name = models.CharField(max_length=255)


class CSUser(models.Model):
    steam_username = models.CharField(max_length=255)
    team = models.ForeignKey(CSTeam, on_delete=models.SET_NULL, null=True)
