from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.request import Request
from common.responses import SuccessResponse
from common.serializers import BaseSerializer
from common.views import OctoXLabsAPIView
from hosts.selectors import search_hosts


class HostView(OctoXLabsAPIView):
    class InputSerializer(serializers.Serializer):
        query = serializers.CharField(allow_null=False)

        class Meta:
            ref_name = "host_input_serializer"

    class OutputSerializer(BaseSerializer):
        class HostSerializer(BaseSerializer):
            hostname = serializers.CharField(source="Hostname")
            ip = serializers.CharField(source="Ip")

            class Meta:
                ref_name = "host_inner_serializer"

        id = serializers.CharField()
        hosts = HostSerializer(many=True)

        class Meta:
            ref_name = "host_output_serializer"

    @swagger_auto_schema(
        responses={
            "200": OutputSerializer(many=True),
            "400": "Bad Request"
        }
    )
    def post(self, request: Request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        hosts = search_hosts(**input_serializer.validated_data)

        output_serializer = self.OutputSerializer(data=hosts, many=True)
        output_serializer.is_valid(raise_exception=True)
        return SuccessResponse(output_serializer.data)

    def get_serializer_class(self):
        return self.InputSerializer
