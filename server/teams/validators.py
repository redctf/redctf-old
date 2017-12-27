import re
from teams.models import Team


def validate_teamname(value):
    if not re.match(r"^[a-zA-Z0-9_]{1,150}$", value):
        raise Exception("Team name invalid")


def validate_teamname_unique(value):
    if Team.objects.filter(name__iexact=value).exists():
        raise Exception('Team name not available')


def validate_token(value):
    if not re.match(r"^[a-zA-Z0-9-]{1,150}$", value):
        raise Exception("Token invalid")
