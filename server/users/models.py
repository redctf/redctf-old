from django.db import models
from teams.models import Team
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    verified = models.BooleanField(default=False)
    team = models.ForeignKey(Team, default=None, null=True, related_name='users', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)