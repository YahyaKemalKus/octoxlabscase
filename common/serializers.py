from pydantic import BaseModel
from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        if isinstance(data, BaseModel):
            return data.dict()
        return data
