import re
from challenges.models import Challenge

def validate_flag(value):
    if not re.match(r"^[a-zA-Z0-9\ \!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]{,100}", value):
        raise Exception('Invalid flag')

def validate_flag_unique(value):
    if Challenge.objects.filter(flag__iexact=value).exists():
        raise Exception('Flag already exists')

def validate_points(value):
    if value < 0:
        raise Exception('Invalid points value')

def validate_title(value):
    if not re.match(r"^[a-zA-Z0-9\ \!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]", value):
        raise Exception('Invalid title')

def validate_description(value):
    if not re.match(r"^[a-zA-Z0-9\ \!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]", value):
        raise Exception('Invalid description')