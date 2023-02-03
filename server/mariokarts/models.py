from django.db import models
from django.contrib import admin
from teams.models import Team

# Create your models here.
class Mariokart(models.Model):
  """
  Mariokart model class.
  """
  guid = models.CharField(max_length=50)
  team = models.ForeignKey(Team, default=None, null=True, related_name='mariokarts', on_delete=models.SET_NULL)
  created = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.guid

class MariokartAdmin(admin.ModelAdmin):
  #This inner class indicates to the admin interface how to display a post
  #See the Django documentation for more information
  list_display = ('guid',)
