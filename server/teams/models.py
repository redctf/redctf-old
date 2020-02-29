from django.db import models
from challenges.models import Challenge
from django.contrib import admin

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
    hidden = models.BooleanField(default=False)
    correct_flags = models.IntegerField(default=0)
    wrong_flags = models.IntegerField(default=0)
    solved = models.ManyToManyField(SolvedChallenge)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class TeamAdmin(admin.ModelAdmin):
    #This inner class indicates to the admin interface how to display a post
    #See the Django documentation for more information
    list_display = ('name', 'token')
