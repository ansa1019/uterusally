from rest_framework import serializers
from userprofile.models import profile
from .models import *


class notificationsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField("get_url")
    action = serializers.SerializerMethodField("get_action")

    class Meta:
        model = Notifications
        fields = "__all__"

    def get_url(self, instance):
        if instance.author:
            nickname = profile.objects.get(user=instance.author).nickname
            return "/author_article_list/" + nickname + "/-created_at"
        elif instance.hashtag:
            return "/searchArticle/" + str(instance.hashtag.hashtag)[1:] + "/-created_at"
        elif instance.post:
            if instance.post.is_official:
                return "/knowledge_article/" + str(instance.post.id)
            else:
                return "/TreatmentArticleGet/" + str(instance.post.id)
        elif instance.gift:
            if instance.gift.giver == instance.user:
                return "/point_use_record"
            else:
                return "/point_get_record"
        elif instance.exchange:
            return "/point_use_record"
        elif instance.systemPoint:
            return "/point_get_record"
        elif instance.blacklist:
            return "/notifications"
        elif instance.product:
            return "/point_exchange"

    def get_action(self, instance):
        if instance.author:
            return "作者貼文更新"
        elif instance.hashtag:
            return "hashtag更新"
        elif instance.post and instance.post.author == instance.user:
            return "發布貼文更新"
        elif instance.post and instance.post.author != instance.user:
            return "收藏貼文更新"
        elif instance.gift:
            return "點數轉贈"
        elif instance.exchange:
            return "點數使用"
        elif instance.systemPoint:
            return "點數獲得"
        elif instance.blacklist:
            return "社群違規"
        elif instance.product:
            return "產品推播"
