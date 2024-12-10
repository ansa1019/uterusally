from rest_framework import serializers
from userdetail.models import postStoraged
from .models import *


class commentVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentVideo
        fields = "__all__"


class commentImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentImage
        fields = "__all__"


class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = "__all__"


class subcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = subcategory
        fields = "__all__"


class TextEditorPostCommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username", read_only=True)
    images = serializers.SerializerMethodField("get_image_url")
    videos = serializers.SerializerMethodField("get_video_url")
    uploaded_images = serializers.ListField(
        required=False,
        child=serializers.ImageField(allow_empty_file=True, use_url=False),
        allow_empty=True,
        allow_null=True,
    )
    uploaded_videos = serializers.ListField(
        required=False,
        child=serializers.FileField(allow_empty_file=True, use_url=False),
        allow_empty=True,
        allow_null=True,
    )
    userdata = serializers.SerializerMethodField("get_nickname")

    class Meta:
        model = TextEditorPostComment
        fields = "__all__"

    def get_image_url(self, instance):
        request = self.context.get("request")
        images = CommentImage.objects.filter(post=instance)
        return [request.build_absolute_uri(image.images.url) for image in images]

    def get_video_url(self, instance):
        request = self.context.get("request")
        Video = CommentVideo.objects.filter(post=instance)
        return [request.build_absolute_uri(video.videos.url) for video in Video]

    def get_nickname(self, instance):
        from userprofile.models import profile

        author = instance.author
        try:
            if author:
                userprofile = profile.objects.get(user=author)
                if (
                    userprofile.user_image
                    and hasattr(userprofile.user_image, "url")
                    and instance.identity != "匿名"
                ):
                    return {
                        "nickname": userprofile.nickname,
                        "image": userprofile.user_image.url,
                    }
                else:
                    url = "user_image/" + userprofile.gender + ".png"
                    return {"nickname": userprofile.nickname, "image": url}
        except:
            return {"nickname": "anonymous", "image": None}

    def create(self, validated_data):
        user = self.context["request"].user
        from .models import TextEditorPost

        if "uploaded_images" in validated_data or "uploaded_videos" in validated_data:
            if "uploaded_images" in validated_data:
                uploaded_images = validated_data.pop("uploaded_images")
            else:
                uploaded_images = None
            if "uploaded_videos" in validated_data:
                uploaded_videos = validated_data.pop("uploaded_videos")
            else:
                uploaded_videos = None
            new_postimage = []
            new_postvideo = []
            post = TextEditorPostComment.objects.create(
                author=user,
                post=validated_data["post"],
                identity=validated_data["identity"],
                body=validated_data["body"],
                top=validated_data["top"],
                desable=validated_data["desable"],
            )
            if uploaded_images:
                for image in uploaded_images:
                    new_postimage.append(
                        CommentImage.objects.create(post=post, images=image)
                    )
            if uploaded_videos:
                for video in uploaded_videos:
                    new_postvideo.append(
                        CommentVideo.objects.create(post=post, videos=video)
                    )

            post.images.set(new_postimage)
            post.videos.set(new_postvideo)

        else:
            print(validated_data)
            post = TextEditorPostComment.objects.create(
                author=user,
                post=validated_data["post"],
                identity=validated_data["identity"],
                body=validated_data["body"],
                top=validated_data["top"],
                desable=validated_data["desable"],
            )

        return post


class PostMetadataSerializer(serializers.ModelSerializer):
    element = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = TextEditorPost
        fields = ["like", "share", "click", "element"]

    def task_checker(self, type_of_task):
        from task.models import task, taskRecord
        if type_of_task == "like":
            type_of_task = "按讚"
        elif type_of_task == "share":
            type_of_task = "分享"

        try:
            d = "每日" + type_of_task
            dt = task.objects.get(type="DAILY", title=d)
            udt, created = taskRecord.objects.get_or_create(user=self.context["request"].user, task=dt)
            if udt.is_done:
                pass
            else:

                progress = udt.progress + 1
                udt.progress = progress
                udt.save()
                if udt.progress == dt.progress:
                    from point.models import point
                    p = point.objects.get(user=self.context["request"].user)
                    p.point += dt.point

                    udt.is_done = True
                    p.save()
                    udt.save()
        except:
            print("DAILY task not found")

        try:
            e = "活動" + type_of_task
            et = task.objects.get(type="EVENT", title=e)
            uet, created = taskRecord.objects.get_or_create(user=self.context["request"].user, task=et)
            if uet.is_done:
                pass
            else:
                progress = uet.progress + 1
                uet.progress = progress
                uet.save()
                if uet.progress == et.progress:
                    from point.models import point
                    p = point.objects.get(user=self.context["request"].user)
                    p.point += et.point

                    uet.is_done = True
                    p.save()
                    uet.save()
        except:
            print("EVENT task not found")
            pass

    def update(self, instance, validated_data):
        element = validated_data.pop("element")
        match element:
            case "like":
                if instance.like.filter(id=self.context["request"].user.id).exists():
                    instance.like.remove(self.context["request"].user)
                else:
                    instance.like.add(self.context["request"].user)
                    self.task_checker("like")
            case "share":
                if instance.share.filter(id=self.context["request"].user.id).exists():
                    instance.share.remove(self.context["request"].user)
                else:
                    instance.share.add(self.context["request"].user)
                    self.task_checker("share")

            case "click":
                if instance.click.filter(id=self.context["request"].user.id).exists():
                    pass
                else:
                    instance.click.add(self.context["request"].user)
        return instance


class TextEditorPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username", read_only=True)
    userdata = serializers.SerializerMethodField("get_nickname")
    category = subcategorySerializer(many=True, required=False)
    html = serializers.SerializerMethodField()
    plain = serializers.SerializerMethodField()
    comments = TextEditorPostCommentSerializer(
        source="textEditorPostComments.all", read_only=True, many=True
    )
    click = serializers.SerializerMethodField("get_click")
    like = serializers.SerializerMethodField("get_like")
    share = serializers.SerializerMethodField("get_share")
    users = serializers.SerializerMethodField("get_users")
    bookmark = serializers.SerializerMethodField("get_bookmark")
    maincate = serializers.SerializerMethodField("get_maincate")

    class Meta:
        model = TextEditorPost
        fields = "__all__"

    def get_maincate(self, instance):
        cate = category.objects.get(name=instance.category.all()[0].main)
        return str(cate.name)

    def get_html(self, instance):
        return str(instance.content.html)

    def get_plain(self, instance):
        return str(instance.content.plain)

    def get_click(self, instance):
        rec = record.objects.filter(article=instance.id)
        return {
            "count": rec.count(),
            "in_user": [
                True if self.context["request"].user in instance.click.all() else False
            ],
        }

    def get_like(self, instance):
        return {
            "count": instance.like.count(),
            "in_user": [
                True if self.context["request"].user in instance.like.all() else False
            ],
        }

    def get_users(self, instance):
        users = []
        for user in instance.click.all():
            if user not in users:
                users.append(user)
        return {
            "count": len(users),
        }

    def get_share(self, instance):
        return {
            "count": instance.share.count(),
            "in_user": [
                True if self.context["request"].user in instance.share.all() else False
            ],
        }

    def get_bookmark(self, instance):
        if self.context["request"].user.is_anonymous:
            return {
                "count": postStoraged.objects.filter(post__id=instance.id).count(),
                "in_user": [False],
            }
        else:
            return {
                "count": postStoraged.objects.filter(post__id=instance.id).count(),
                "in_user": [
                    (
                        True
                        if postStoraged.objects.filter(
                            post__id=instance.id, user=self.context["request"].user
                        ).count()
                        > 0
                        else False
                    )
                ],
            }

    def get_nickname(self, instance):
        from userprofile.models import profile

        author = instance.author
        if author:
            userprofile = profile.objects.get(user=author)
            if userprofile.user_image and hasattr(userprofile.user_image, "url"):
                return {
                    "nickname": userprofile.nickname,
                    "image": userprofile.user_image.url,
                }
            else:
                url = "user_image/" + userprofile.gender + ".png"
                return {"nickname": userprofile.nickname, "image": url}


class queryPostSerializer(TextEditorPostSerializer):
    class Meta:
        model = TextEditorPost
        fields = "__all__"


class hashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextEditorPost
        fields = ["hashtag"]


class recordSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField("get_time")

    class Meta:
        model = record
        fields = "__all__"

    def get_time(self, instance):
        if instance.end:
            time = int((instance.end - instance.start).total_seconds())
            return time


class pollsSerializer(serializers.ModelSerializer):
    class Meta:
        model = polls
        fields = "__all__"


class optionSerializer(serializers.ModelSerializer):

    class Meta:
        model = option
        fields = "__all__"


class voteSerializer(serializers.ModelSerializer):

    class Meta:
        model = vote
        fields = "__all__"
