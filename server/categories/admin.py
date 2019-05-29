from django.contrib import admin
from categories.models import *

admin.site.register(Category, CategoryAdmin)
