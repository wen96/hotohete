# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class HotoheteSettings(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)
