import re
from categories.models import Category

def validate_name(value):
    if not re.match(r"^[a-zA-Z]{,50}", value):
        raise Exception('Invalid category name')

def validate_name_unique(value):
    if Category.objects.filter(name__iexact=value).exists():
        raise Exception('Category already exists')
