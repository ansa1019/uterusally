from rest_framework import serializers
from content.serializer import TextEditorPostSerializer
from .models import *


class postStoragedSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField(method_name="get_post")

    class Meta:
        model = postStoraged
        fields = "__all__"

    def get_post(self, obj):
        return [str(post.id) for post in obj.post.all()]


class postlistSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField(method_name="get_post")

    class Meta:
        model = postStoraged
        fields = "__all__"

    def get_post(self, obj):
        post = TextEditorPost.objects.filter(
            title__in=[post.title for post in obj.post.all()]
        )
        return TextEditorPostSerializer(
            post, many=True, context={"request": self.context["request"]}
        ).data
