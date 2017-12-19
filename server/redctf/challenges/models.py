from django.db import models

# Create your models here.
class Challenge(models.Model):
  """
  Challenge model class.
  """
  flag = models.CharField(max_length=100)