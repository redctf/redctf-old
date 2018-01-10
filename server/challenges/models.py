from django.db import models
from categories.models import Category


# Create your models here.
class Challenge(models.Model):
  """
  Challenge model class.
  """
  category = models.ForeignKey(Category, default=None, null=True, on_delete=models.CASCADE, related_name='categories')
  points = models.IntegerField(default=0)
  flag = models.CharField(max_length=100)