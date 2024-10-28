from rest_framework import serializers
from content.serializer import TextEditorPostSerializer
from .models import *


class postStoragedSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField(method_name="get_post")
    image = serializers.SerializerMethodField(method_name="get_image")

    class Meta:
        model = postStoraged
        fields = "__all__"

    def get_post(self, obj):
        return [str(post.id) for post in obj.post.all()]

    def get_image(self, obj):
        post = obj.post.first()
        if post:
            request = self.context.get('request')
            return request.build_absolute_uri(post.index_image.url)
        else:
            return None


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
