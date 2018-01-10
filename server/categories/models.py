from django.db import models


# Create your models here.
class Category(models.Model):
  """
  Challenge model class.
  """
  name = models.CharField(max_length=50)
  created = models.DateTimeField(auto_now_add=True)