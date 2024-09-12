from django.templatetags.static import static
from rest_framework import serializers
from userprofile.models import profile
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"


class previousChatSerializer(serializers.ModelSerializer):
    is_user = serializers.SerializerMethodField("get_user")
    user_image = serializers.SerializerMethodField("get_image")

    class Meta:
        model = Chat
        fields = "__all__"

    def get_user(self, instance):
        return True if self.context["request"].user == instance.user else False

    def get_image(self, instance):
        userProfile = profile.objects.get(user=instance.user)
        if instance.identity != "匿名" and userProfile.user_image:
            return userProfile.user_image.url
        else:
            return static(userProfile.gender + ".png")
