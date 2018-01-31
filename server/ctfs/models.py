from django.db import models

class Ctf(models.Model):
  """
  Challenge model class.
  """
  start = models.DateTimeField()
  end = models.DateTimeField()
  created = models.DateTimeField(auto_now_add=True)