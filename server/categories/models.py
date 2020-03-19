from django.db import models
from django.contrib import admin

# Create your models here.
class Category(models.Model):
  """
  Challenge model class.
  """
  name = models.CharField(max_length=50)
  created = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.name

class CategoryAdmin(admin.ModelAdmin):
  #This inner class indicates to the admin interface how to display a post
  #See the Django documentation for more information
  list_display = ('name',)
