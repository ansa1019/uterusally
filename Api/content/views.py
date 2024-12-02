import random
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django.db.models import Count, Avg, F
from .models import *
from .serializer import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# from .filters import contentPostFilter
# Create your views here.

"""


let get_data = (url) =>{
    return fetch(url).then(response =>
        response.json()
    )
}

get_data(url).then(json => {
        create_chart(json, customized, target_element); //get new chart while get new sensor data.
});

  
const delta = quill.clipboard.convert(obj[0].content)

quill.setContents(delta, 'silent')

"""


class categoryView(viewsets.ModelViewSet):
    queryset = category.objects.all()
    serializer_class = categorySerializer


class subcategoryView(viewsets.ModelViewSet):
    queryset = subcategory.objects.all()
    serializer_class = subcategorySerializer


class PostMetadataView(viewsets.ModelViewSet):
    queryset = TextEditorPost.objects.all()
    serializer_class = PostMetadataSerializer


class queryPostView(viewsets.ModelViewSet):
    queryset = TextEditorPost.objects.all()
    serializer_class = queryPostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["title", "author", "category__category_name"]
    search_fields = ["title", "author__username", "category__name", "hashtag"]

    ordering_fields = ["created_at", "click"]

    def get_queryset(self):
        return self.queryset.filter(is_temporary=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        if request.query_params.get("ordering") == "click":
            # print("click")
            queryset = queryset.order_by("id").distinct()
            queryset = queryset.filter(is_temporary=False)
            queryset = queryset.annotate(
                click_count=Count("click", distinct=True)
            ).order_by("click_count")
            # print(queryset.values("click_count"))
            serializer = self.serializer_class(
                queryset[::-1], many=True, context={"request": request}
            )
            return Response(serializer.data)
        elif request.query_params.get("ordering") == "-click":
            # print("-click")
            queryset = queryset.order_by("id").distinct()
            queryset = queryset.filter(is_temporary=False)
            queryset = queryset.annotate(
                click_count=Count("click", distinct=True)
            ).order_by("click_count")
            # print(queryset.values("click_count"))
            serializer = self.serializer_class(
                queryset[::-1], many=True, context={"request": request}
            )
            return Response(serializer.data)
        elif request.query_params.get("ordering") == "created_at":
            # print("created_at")
            queryset = queryset.order_by("created_at")
        elif request.query_params.get("ordering") == "-created_at":
            # print("-created_at")
            queryset = queryset.order_by("created_at")
            serializer = self.serializer_class(
                queryset[::-1], many=True, context={"request": request}
            )
            return Response(serializer.data)
        # else:
        # print(request.query_params.get("ordering"))
        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def filter_queryset(self, queryset):

        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset


class getTmpPostView(viewsets.ModelViewSet):
    queryset = TextEditorPost.objects.all()
    serializer_class = TextEditorPostSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(
            is_temporary=True, is_official=False, author=request.user
        )
        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class PostGetOfficialView(viewsets.ModelViewSet):
    queryset = TextEditorPost.objects.all()
    serializer_class = TextEditorPostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["title", "author", "subcategory__category_name"]
    search_fields = [
        "title",
        "author__username",
        "subcategory__name",
        "created_at",
        "hash_tag",
    ]

    ordering_fields = ["created_at", "click"]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_temporary=False, is_official=True)
        queryset = self.filter_queryset(queryset)

        if request.query_params.get("ordering") == "click":
            queryset = queryset.order_by("id").distinct()
            queryset = queryset.filter(is_temporary=False)
            queryset = queryset.annotate(
                click_count=Count("click", distinct=True)
            ).order_by("click_count")
            serializer = self.serializer_class(
                queryset[::-1], many=True, context={"request": request}
            )
            return Response(serializer.data)
        elif request.query_params.get("ordering") == "-click":
            queryset = queryset.order_by("id").distinct()
            queryset = queryset.filter(is_temporary=False)
            queryset = queryset.annotate(
                click_count=Count("click", distinct=True)
            ).order_by("click_count")
            serializer = self.serializer_class(
                queryset, many=True, context={"request": request}
            )
            return Response(serializer.data)

        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class orderByClickView(viewsets.ModelViewSet):
    queryset = TextEditorPost.objects.all()
    serializer_class = TextEditorPostSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        queryset = (
            queryset.filter(is_official=False, is_temporary=False)
            .annotate(click_count=Count("click"))
            .order_by("-click_count")
        )
        data = queryset.values(
            "title",
            "id",
        )

        return Response({"data": data})


class orderByClickOfficialView(viewsets.ModelViewSet):
    queryset = TextEditorPost.objects.all()
    serializer_class = TextEditorPostSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        queryset = (
            queryset.filter(is_official=True, is_temporary=False)
            .annotate(click_count=Count("click"))
            .order_by("-click_count")
        )

        # print(queryset.values("title", "id"))
        data = queryset.values("title", "id")

        return Response({"data": data})


class textEditorPostSerializerView(viewsets.ModelViewSet):
    queryset = TextEditorPost.objects.all()
    serializer_class = TextEditorPostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["title", "author", "subcategory__category_name"]
    search_fields = ["title", "author__username",
                     "subcategory__name", "hashtag"]

    ordering_fields = ["created_at", "click"]

    def list(self, request, *args, **kwargs):
        """
        日後如果輔大那邊真的很需要定時發文的部分，可在這邊加入celery的task，這邊的celery task可以用來定時發文
        如果不會設定celery task，就在model裡面加入一個field，用來判斷是否為定時發文，然後在這邊加入一個判斷式，如果是定時發文就發文
        example:
        #/content.models.py

        class TextEditorPost(models.Model):
            **exsit field**
            post_time = models.DateTimeField(null=True, blank=True)
            desable = models.BooleanField(default=False) #! True

        #./
        def list(self, request, *args, **kwargs):
            get_post_if_not_post_because_of_time = self.queryset.filter(post_time__gt=now(), desable=False)
            for post in get_post_if_not_post_because_of_time:
                if post.post_time > now() and post.desable == False:
                    post.desable == True
                    post.save()

        """
        queryset = self.queryset.filter(is_temporary=False, is_official=False)
        queryset = self.filter_queryset(queryset)

        if request.query_params.get("ordering") == "click":
            # print("click")
            queryset = queryset.order_by("id").distinct()
            queryset = queryset.filter(is_temporary=False)
            queryset = queryset.annotate(
                click_count=Count("click", distinct=True)
            ).order_by("click_count")
            # print(queryset.values("click_count"))
            serializer = self.serializer_class(
                queryset, many=True, context={"request": request}
            )
            return Response(serializer.data)
        elif request.query_params.get("ordering") == "-click":
            # print("-click")
            queryset = queryset.order_by("id").distinct()
            queryset = queryset.filter(is_temporary=False)
            queryset = queryset.annotate(
                click_count=Count("click", distinct=True)
            ).order_by("click_count")
            # print(queryset.values("click_count"))
            serializer = self.serializer_class(
                queryset[::-1], many=True, context={"request": request}
            )
            return Response(serializer.data)
        elif request.query_params.get("ordering") == "-created_at":
            # print("-created_at")
            queryset = queryset.order_by("created_at")
            serializer = self.serializer_class(
                queryset[::-1], many=True, context={"request": request}
            )
            return Response(serializer.data)
        elif request.query_params.get("ordering") == "created_at":
            # print("created_at")
            queryset = queryset.order_by("created_at")
            serializer = self.serializer_class(
                queryset, many=True, context={"request": request}
            )
            return Response(serializer.data)
        else:
            serializer = self.serializer_class(
                queryset, many=True, context={"request": request}
            )
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        基本上創建文章應該是不太會動了，但如果需要做notifications的話可以在這邊加入trigger 的decorator

        """
        from .models import subcategory
        from django.contrib.auth.models import User

        author = User.objects.get(username=request.user.username)
        cate = subcategory.objects.get(name=request.data["category"])
        try:
            identity = request.data["identity"]
        except:
            identity = request.user.username
        try:
            index_image = request.data["index_image"]
        except:
            index_image = "textEditorPost_index_image/img_" + \
                str(random.randint(1, 4))+".png"
        post_obj = TextEditorPost.objects.create(
            author=author,
            identity=identity,
            content=request.data["content"],
            title=request.data["title"],
            is_temporary=request.data["is_temporary"],
            is_official=request.data["is_official"],
        )
        post_obj.category.add(cate)
        post_obj.index_image = index_image
        serializer = self.serializer_class(
            post_obj, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def update(self, request, *args, **kwargs):
        from .models import subcategory
        from django.contrib.auth.models import User

        author = User.objects.get(username=request.user.username)

        try:
            # print("request.data['category']:" + request.data["category"])
            if request.data["category"]:
                cate = subcategory.objects.get(name=request.data["category"])
            else:
                cate = None
        except:
            cate = None

        try:
            identity = request.data["identity"]
        except:
            identity = request.user.username
        post_obj = TextEditorPost.objects.get(id=self.kwargs.get('pk'))
        post_obj.author = author
        try:
            post_obj.content = request.data["content"]
        except:
            pass
        try:
            post_obj.title = request.data["title"]
        except:
            pass
        try:
            post_obj.index_image = request.data["index_image"]
        except:
            pass
        post_obj.identity = identity
        try:
            post_obj.is_official = request.data["is_official"]
        except:
            pass
        try:
            post_obj.is_temporary = request.data["is_temporary"]
        except:
            pass
        if cate:
            # print(cate)
            post_obj.category.clear()
            post_obj.category.add(cate)
        elif cate == None:
            post_obj.category.clear()
        post_obj.save()
        serializer = self.serializer_class(
            post_obj, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error_messages)


class testTextEditorPostCommentSerializerView(viewsets.ModelViewSet):
    queryset = TextEditorPostComment.objects.all()
    serializer_class = TextEditorPostCommentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filter_fields = ["post", "author", "top"]

    def post(self, request, *args, **kwargs):
        user = request.user
        dt = task.objects.get(type="DAILY", title="每日回覆")
        udt = taskRecord.objects.get(user=request.user, task=dt)
        if udt.is_done:
            pass
        else:
            progress = udt.progress + 1
            udt.progress = progress
            udt.save()
            if udt.progress == dt.progress:
                udt.is_done = True
                udt.save()

        et = task.objects.get(type="EVENT", title="活動回覆")
        uet = taskRecord.objects.get(user=request.user, task=et)
        if uet.is_done:
            pass
        else:
            progress = uet.progress + 1
            uet.progress = progress
            uet.save()
            if uet.progress == et.progress:
                uet.is_done = True
                uet.save()

        return Response(request.data)


class userGetSelfCommentView(viewsets.ModelViewSet):
    queryset = TextEditorPostComment.objects.all()
    serializer_class = TextEditorPostCommentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filter_fields = ["post", "author", "top"]

    # def get_queryset(self):
    #     if self.request.user.is_anonymous:
    #         return Response({'error': 'user is anonymous'})
    #
    #     else:
    #         user = self.request.user
    #         return TextEditorPostComment.objects.filter(author=user)

    def list(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({"error": "user is anonymous"})

        else:
            user = self.request.user
            return super().list(request, *args, **kwargs)


class getTagClickView(viewsets.ModelViewSet):
    """
    基本上是拿來做熱門標籤的
    """

    queryset = subcategory.objects.all()
    serializer_class = TextEditorPostSerializer

    def list(self, request, *args, **kwargs):
        sort_click = subcategory.objects.annotate(
            click_count=Count("texteditorpost__click")
        ).order_by("-click_count")

        # print(sort_click.values("name"))
        return Response(sort_click.values_list("name", flat=True))


class userGetSelfPostView(viewsets.ModelViewSet):
    """
    filter使用者自己的文章
    """

    queryset = TextEditorPost.objects.all()
    serializer_class = TextEditorPostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filter_fields = ["title", "author", "subcategory__category_name"]

    def list(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({"error": "user is anonymous"})

        else:
            user = self.request.user
            query = self.queryset.filter(author=user)
            serializer = self.serializer_class(
                query, many=True, context={"request": request}
            )
            return Response(serializer.data)
            # return super().list(request, *args, **kwargs)


class userGetBookmarkView(viewsets.ModelViewSet):
    queryset = TextEditorPost.objects.all()
    serializer_class = TextEditorPostSerializer

    """
        filter使用者自己的收藏文章，但這邊的流程現在不同了，可能要研究一下，目前已知可能會跟現有的儲存有衝突
    """

    def list(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({"error": "user is anonymous"})

        else:
            user = self.request.user

            query = self.queryset.filter(bookmark=user)
            subs = []

            for title, username in zip(
                query.values("title"), query.values("author__username")
            ):
                subs.append(
                    [{"title": title["title"], "author": username["author__username"]}]
                )
            return Response({"subscribe": subs})


class hashTagView(viewsets.ModelViewSet):
    queryset = TextEditorPost.objects.all()
    serializer_class = hashTagSerializer

    """
    儲存hashtag所使用，使用,來進行分割
    """

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        hashtags = []
        for i in queryset.values("hashtag"):
            if i["hashtag"]:
                for ht in i["hashtag"].split(","):
                    hashtags.append(ht)
        hashtags = list(
            dict.fromkeys(sorted(hashtags, key=hashtags.count, reverse=True))
        )

        return Response({"hashtags": hashtags})


class officialPostTempSaveView(viewsets.ModelViewSet):
    queryset = TextEditorPost.objects.all()
    serializer_class = TextEditorPostSerializer
    """
    給官方文章暫存所使用
    """

    def create(self, request, *args, **kwargs):
        from .models import subcategory
        from django.contrib.auth.models import User

        author = User.objects.get(username=request.user.username)
        cate = subcategory.objects.get(name=request.data["category"])
        try:
            identity = request.data["identity"]
        except:
            identity = request.user.username

        # print(request.data["is_official"])

        post_obj = TextEditorPost.objects.create(
            author=author,
            identity=identity,
            content=request.data["content"],
            title=request.data["title"],
            index_image=request.data["index_image"],
            is_temporary=request.data["is_temporary"],
            is_official=request.data["is_official"],
        )
        post_obj.category.add(cate)
        serializer = self.serializer_class(
            post_obj, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def update(self, request, *args, **kwargs):
        from .models import subcategory
        from django.contrib.auth.models import User

        author = User.objects.get(username=request.user.username)
        try:
            # print("request.data['category']:" + request.data["category"])
            if request.data["category"]:
                cate = subcategory.objects.get(name=request.data["category"])
            else:
                cate = None
        except:
            cate = None

        try:
            identity = request.data["identity"]
        except:
            identity = request.user.username
        post_obj = TextEditorPost.objects.get(id=self.kwargs.get('pk'))
        post_obj.author = author

        try:
            post_obj.content = request.data["content"]
        except:
            pass
        try:
            post_obj.title = request.data["title"]
        except:
            pass
        try:
            post_obj.index_image = request.data["index_image"]
        except:
            pass
        post_obj.identity = identity
        try:
            post_obj.is_official = request.data["is_official"]
        except:
            pass
        try:
            post_obj.is_temporary = request.data["is_temporary"]
        except:
            pass

        if cate:
            post_obj.category.clear()
            post_obj.category.add(cate)
        elif cate == None:
            post_obj.category.clear()
        post_obj.save()
        serializer = self.serializer_class(
            post_obj, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class getOfficialTempPostView(getTmpPostView):
    """
    獲取官方文章暫存
    """

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(
            is_official=True, is_temporary=True, author=request.user
        )
        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class getCategoryView(viewsets.ModelViewSet):
    """
    獲取分類，與hashtag不同，是指文章的大標小標相關物件
    """

    queryset = category.objects.all()
    serializer_class = categorySerializer

    def list(self, request, *args, **kwargs):
        sub = subcategory.objects.all()
        cate = {}
        for s in sub:
            cate[s.name] = s.main.name

        return Response(cate)


class getRecordView(viewsets.ModelViewSet):
    queryset = record.objects.all()
    serializer_class = recordSerializer

    def list(self, request, *args, **kwargs):
        articles = TextEditorPost.objects.all()
        records = {}
        for article in articles:
            rec = record.objects.filter(
                article=article).exclude(end__isnull=True)
            if rec:
                time = rec.annotate(time=Avg(F("end") - F("start"))).values("time")[0][
                    "time"
                ]
                hours, remainder = divmod(time.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                hours_str = f"{hours}時 " if hours else ""
                minutes_str = f"{minutes}分 " if minutes else ""
                seconds_str = f"{seconds}秒" if seconds and not hours_str else ""
                time_str = f"{hours_str}{minutes_str}{seconds_str}"
            else:
                time_str = "尚無"
            records[article.id] = {"time": time_str, "click": rec.count()}
        return Response(records)


class recordView(viewsets.ModelViewSet):
    queryset = record.objects.all()
    serializer_class = recordSerializer


"""
這裡都是投票相關的東西
"""


class pollsView(viewsets.ModelViewSet):
    queryset = polls.objects.all()
    serializer_class = pollsSerializer


class optionView(viewsets.ModelViewSet):
    queryset = option.objects.all()
    serializer_class = optionSerializer


class voteView(viewsets.ModelViewSet):
    queryset = vote.objects.all()
    serializer_class = voteSerializer
