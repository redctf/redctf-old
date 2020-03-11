from django.db import models
from challenges.models import Challenge
from users.models import User
from django.contrib import admin

# Create your models here.


class Container(models.Model):
    """
    Container model class.
    """
    name = models.CharField(max_length=512)
    challenge = models.ForeignKey(
        Challenge, default=None, null=True, on_delete=models.CASCADE, related_name='challenges')
    user = models.ForeignKey(
        User, default=None, null=True, on_delete=models.CASCADE, related_name='users')
    created = models.DateTimeField(auto_now_add=True)


class ContainerAdmin(admin.ModelAdmin):
    # This inner class indicates to the admin interface how to display a post
    # See the Django documentation for more information
    list_display = ('name', 'challenge_title', 'challenge', 'created',
                    'user')

    def challenge_title(self, obj):
        return obj.challenge.title
    challenge_title.short_desription = 'Challenge Title'
    challenge_title.admin_order_field = 'challenge_title'
