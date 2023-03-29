from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import Count
from categories.models import Category
from django.contrib import admin

def user_directory_path(instance, filename): 
  # file will be uploaded to MEDIA_ROOT/uploads/challenge_<id>/<filename>
  return 'uploads/chall_{0}/{1}'.format(instance.id, filename)

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name

# Create your models here.
class Challenge(models.Model):
  """
  Challenge model class.
  """
  title = models.CharField(max_length=100)
  description = models.CharField(max_length=512)
  category = models.ForeignKey(Category, default=None, null=True, on_delete=models.CASCADE, related_name='categories')
  points = models.IntegerField(default=0)
  flag = models.CharField(max_length=100)
  hosted = models.BooleanField(default=False)
  fileUpload = models.BooleanField(default=False)
  imageName = models.CharField(max_length=100, default=None, null=True, blank=True)
  ports = models.CharField(max_length=100, default=None, null=True, blank=True)
  pathPrefix = models.CharField(max_length=100, default=None, null=True, blank=True)
  #upload = models.FileField(upload_to=user_directory_path, default=None, null=True, blank=True)
  upload = models.FileField(storage=OverwriteStorage(), upload_to=user_directory_path, default=None, null=True, blank=True)
  created = models.DateTimeField(auto_now_add=True)
  hackart = models.BooleanField(default=False)
  
  def solved_count(self):
    return self.solvedchallenge_set.count()

  def __str__(self):
    return self.title + ' - ' + str(self.points) + 'pts' 
    #return 'id:' + str(self.id) + ' - ' + self.title + '_' + str(self.points) 


class ChallengeAdmin(admin.ModelAdmin):
  #This inner class indicates to the admin interface how to display a post
  #See the Django documentation for more information
  list_display = ('get_category', 'title', 'points', 'flag', 'pathPrefix', 'upload')

  def get_category(self, obj):
    return obj.category.name
  get_category.short_description = 'Category'
  get_category.admin_order_field = 'category__name'
