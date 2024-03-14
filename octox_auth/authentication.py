import base64

from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from typing import Optional, Tuple

from common.exceptions import TokenError
from octoxlabscase import settings

import jwt


class OctoXLabsAuth(BaseAuthentication):
    USER_MODEL = get_user_model()

    def authenticate(self, request) -> Optional[Tuple[USER_MODEL, dict]]:
        """Entrypoint for Django Rest Framework"""
        token = self.get_token(request)
        if token is None:
            raise exceptions.AuthenticationFailed()
        source, encrypted_data = token
        try:
            if source == b"Bearer":
                payload = self.get_jwt_payload(encrypted_data)
            elif source == bytes(settings.AUTH_HEADER_PREFIX, "utf-8"):
                payload = self.get_octox_payload(encrypted_data)
            else:
                raise NotImplementedError()
        except TokenError:
            raise exceptions.AuthenticationFailed()
        username = payload["username"]
        user = self.USER_MODEL.objects.get(username=username)
        return user, token

    @staticmethod
    def get_jwt_payload(encrypted_data):
        try:
            return jwt.decode(encrypted_data, settings.SECRET_KEY, algorithms="HS256",
                              options={"verify_signature": True})
        except jwt.PyJWTError:
            raise TokenError

    @staticmethod
    def get_octox_payload(encrypted_data):
        try:
            username = base64.b64decode(encrypted_data).decode()
            return {"username": username}
        except jwt.PyJWTError:
            raise TokenError

    @staticmethod
    def get_token(request):
        auth = get_authorization_header(request).split()
        if not auth or force_str(auth[0]) not in [settings.AUTH_HEADER_PREFIX, "Bearer"]:
            return None

        if len(auth) == 1:
            msg = _("Invalid Authorization header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _(
                "Invalid Authorization header. Credentials string "
                "should not contain spaces."
            )
            raise exceptions.AuthenticationFailed(msg)
        return auth
