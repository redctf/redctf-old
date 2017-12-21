import re
from users.models import User

def validate_username(value):
    if not re.match(r"^[a-zA-Z0-9_]{1,150}$", value):
        raise Exception("Username invalid")
    elif User.objects.filter(username__iexact=value).exists():
        raise Exception('Username not available')


def validate_email(value):
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
        raise Exception("Email invalid")
    elif User.objects.filter(email__iexact=value).exists():
        raise Exception('Email already registered')


def validate_password(value):
    if not re.match(r"^[a-zA-Z0-9 !\"#$%&'()*+,-.\/:;<=>?@[\\\]^_`{|}~]{12,}$", value):
        raise Exception('Password invalid. Must contain an uppercase letter, lowercase letter, a digit, a special character and be at least 12 characters long')