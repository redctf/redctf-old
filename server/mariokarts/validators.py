import re
from mariokarts.models import Mariokart

def validate_name(value):
    if not re.match(r"^[a-zA-Z0-9\-]{,50}", value):
        raise Exception('Invalid mariokart name')

def validate_name_unique(value):
    if Mariokart.objects.filter(name__iexact=value).exists():
        raise Exception('Mariokart already exists')

def validate_mariokart_exists(id_value):
    if not Mariokart.objects.filter(id=id_value).exists():
        raise Exception('Mariokart does not exist')
