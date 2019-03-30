from django.contrib import admin
from challenges.models import *

admin.site.register(Challenge, ChallengeAdmin)
