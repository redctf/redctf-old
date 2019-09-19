from django.contrib import admin
from containers.models import *

# Register your models here.
admin.site.register(Container, ContainerAdmin)
