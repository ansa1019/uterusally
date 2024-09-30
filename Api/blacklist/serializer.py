from rest_framework import serializers
from .models import *


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class BanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ban
        fields = "__all__"


class BlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blacklist
        fields = "__all__"