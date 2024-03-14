from rest_framework.generics import GenericAPIView

from octox_auth.authentication import OctoXLabsAuth


class OctoXLabsAPIView(GenericAPIView):
    authentication_classes = [OctoXLabsAuth]
