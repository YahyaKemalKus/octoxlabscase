from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from common.responses import SuccessResponse, ErrorResponse
from octox_auth.services import authenticate


class AuthView(GenericAPIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField(allow_null=False, allow_blank=False)
        password = serializers.CharField(allow_null=False, allow_blank=False)

        class Meta:
            ref_name = "auth_input_serializer"

    class OutputSerializer(serializers.Serializer):
        token = serializers.CharField(allow_null=False, allow_blank=False)

        class Meta:
            ref_name = "auth_output_serializer"

    @swagger_auto_schema(
        responses={
            "200": OutputSerializer,
            "400": "Bad Request"
        }
    )
    def post(self, request: Request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        octoxlabs_token = authenticate(**input_serializer.validated_data)
        if octoxlabs_token is None:
            return ErrorResponse(data=_("Invalid credentials."))

        output_serializer = self.OutputSerializer(data={"token": octoxlabs_token})
        output_serializer.is_valid(raise_exception=True)
        return SuccessResponse(output_serializer.data)

    def get_serializer_class(self):
        return self.InputSerializer
