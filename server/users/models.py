from django.db import models
from teams.models import Team
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    verified = models.BooleanField(default=False)
    team = models.ForeignKey(Team, default=None, null=True, on_delete=models.SET_NULL)