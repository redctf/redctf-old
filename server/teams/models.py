from django.db import models
from challenges.models import Challenge

# Create your models here.
class SolvedChallenge(models.Model):
    """
    Team solved challenge model
    """
    challenge = models.ForeignKey(Challenge, default=None, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


# Create your models here.
class Team(models.Model):
    """
    Team model class.
    """
    name = models.CharField(max_length=150, unique=True)
    token = models.CharField(default=None, max_length=150, unique=True)
    points = models.IntegerField(default=0)
    correct_flags = models.IntegerField(default=0)
    wrong_flags = models.IntegerField(default=0)
    solved = models.ManyToManyField(SolvedChallenge)
    created = models.DateTimeField(auto_now_add=True)
