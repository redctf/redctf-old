import re
from users.models import User

def validate_username(value):
    if not re.match(r"^[a-zA-Z0-9_]{1,150}$", value):
        raise Exception("Username invalid")

def validate_user_is_authenticated(user):
    if user.is_anonymous:
        raise Exception('Not authenticated')

def validate_user_is_admin(user):
    validate_user_is_authenticated(user)
    if not user.is_superuser:
        raise Exception('Administrator permission required')

def validate_username_unique(value):
    if User.objects.filter(username__iexact=value).exists():
        raise Exception('Username not available')

def validate_email(value):
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
        raise Exception("Email invalid")

def validate_email_unique(value):
    if User.objects.filter(email__iexact=value).exists():
        raise Exception('Email already registered')


def validate_password(value):
    if not re.match(r"^[a-zA-Z0-9\ \!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]{12,}$", value):
        raise Exception('Password invalid. Must contain an uppercase letter, lowercase letter, a digit, a special character and be at least 12 characters long')