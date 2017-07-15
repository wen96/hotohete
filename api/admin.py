# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import CSTeam, CSUser, HotoheteSettings


admin.site.register(CSTeam)
admin.site.register(CSUser)
admin.site.register(HotoheteSettings)
