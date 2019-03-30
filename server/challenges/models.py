from django.db import models
from categories.models import Category
from django.contrib import admin


# Create your models here.
class Challenge(models.Model):
  """
  Challenge model class.
  """
  category = models.ForeignKey(Category, default=None, null=True, on_delete=models.CASCADE, related_name='categories')
  points = models.IntegerField(default=0)
  flag = models.CharField(max_length=100)
  created = models.DateTimeField(auto_now_add=True)

class ChallengeAdmin(admin.ModelAdmin):
  #This inner class indicates to the admin interface how to display a post
  #See the Django documentation for more information
  list_display = ('category', 'points', 'flag')
