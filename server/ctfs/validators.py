import re
from ctfs.models import Ctf

def validate_start(value):
    if value < 0:
        raise Exception('Invalid start time')

def validate_end(value):
    if value < 0:
        raise Exception('Invalid end time')

def validate_ctf_exists(id_value):
    if not Ctf.objects.filter(id=id_value).exists():
        raise Exception('Ctf does not exist')
