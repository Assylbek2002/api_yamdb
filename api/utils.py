import datetime
import random

from django.core.validators import MaxValueValidator
from rest_framework_simplejwt.tokens import RefreshToken


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def code_generator():
    code = random.randint(1000000, 9999999)
    return code


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token)
    }