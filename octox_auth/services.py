import base64
from typing import Optional

import jwt
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth.models import AbstractUser

from octoxlabscase import settings


def authenticate(
        *,
        username: str,
        password: str
) -> Optional[str]:
    user = validate_credentials_and_get_user(username=username, password=password)
    if user is None:
        return None
    elif user.username == settings.OCTOXLABS_SUPERUSER_NAME:
        return generate_octoxlabs_token(username=username)
    else:
        return generate_jwt_token(username=username)


def validate_credentials_and_get_user(
        *,
        username: str,
        password: str
) -> Optional[AbstractUser]:
    user = django_authenticate(username=username, password=password)
    return user


def generate_octoxlabs_token(
        *,
        username: str
):
    conv_bytes = bytes(username, 'utf-8')
    encoded_str = base64.b64encode(conv_bytes).decode()
    octoxlabs_token = f"{settings.AUTH_HEADER_PREFIX} {encoded_str}"
    return octoxlabs_token


def generate_jwt_token(
        *,
        username: str
):
    # expiration time etc. can be set and be validated. It is just a POC.
    jwt_token = jwt.encode({"username": username}, settings.SECRET_KEY, algorithm="HS256")
    octoxlabs_token = f"Bearer {jwt_token}"
    return octoxlabs_token
