from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from content.models import TextEditorPost
from .models import *
from .serializer import *

# Create your views here.


class postStoragedViewSet(viewsets.ModelViewSet):
    queryset = postStoraged.objects.all()
    serializer_class = postStoragedSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if postStoraged.objects.filter(
            user=request.user, storage_name=data["storage_name"]
        ).exists():
            poststorage = postStoraged.objects.get(
                user=request.user, storage_name=data["storage_name"])
            post_id = data["post_id"]
            p = TextEditorPost.objects.get(id=post_id)
            count = postStoraged.objects.filter(post=p).count()

            post_t = [post.title for post in poststorage.post.all()]
            # print(post_t)
            if p.title in post_t:
                poststorage.post.remove(p)
                poststorage.save()
                if count == 1:
                    p.bookmark.remove(request.user)
                    p.save()
                return Response({"message": "移除成功"}, status=status.HTTP_200_OK)
            else:
                poststorage.post.add(p)
                poststorage.save()
                return Response({"message": "新增成功"}, status=status.HTTP_200_OK)
        else:
            poststorage = postStoraged.objects.create(
                user=request.user, storage_name=data["storage_name"]
            )
            return Response(poststorage.id, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = postStoraged.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        poststorage = postStoraged.objects.get(
            user=request.user, storage_name=data["storage_name"]
        )
        if "new_name" in data:
            poststorage.storage_name = data["new_name"]
            poststorage.save()
            return Response(
                {"message": "資料夾名稱修改成功"}, status=status.HTTP_200_OK
            )
        else:
            post_id = data["post_id"]
            p = TextEditorPost.objects.get(id=post_id)
            if p in poststorage.post.all():
                poststorage.post.remove(p)
            else:
                poststorage.post.add(p)
            return Response({"message": "資料夾更新成功"}, status=status.HTTP_200_OK)


class postlistViewSet(viewsets.ModelViewSet):
    queryset = postStoraged.objects.all()
    serializer_class = postlistSerializer

    def list(self, request, *args, **kwargs):
        queryset = postStoraged.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
