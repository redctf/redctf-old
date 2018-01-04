import re
from challenges.models import Challenge

def validate_flag(value):
    if not re.match(r"^[a-zA-Z0-9\ \!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]{,100}", value):
        raise Exception('Wrong flag')

def validate_flag_unique(value):
    if Challenge.objects.filter(flag__iexact=value).exists():
        raise Exception('Flag already exists')

def validate_points(value):
    if value < 0:
        raise Exception('Invalid points value')
