from django.contrib import admin
from teams.models import *

admin.site.register(Team, TeamAdmin)
