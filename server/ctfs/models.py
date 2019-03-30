from django.db import models
from django.contrib import admin

class Ctf(models.Model):
  """
  Challenge model class.
  """
  start = models.DateTimeField()
  end = models.DateTimeField()
  created = models.DateTimeField(auto_now_add=True)

class CtfAdmin(admin.ModelAdmin):
  #This inner class indicates to the admin interface how to display a post
  #See the Django documentation for more information
  list_display = ('start', 'end')
