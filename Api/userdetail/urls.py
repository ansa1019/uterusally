from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "userdetail"

router = DefaultRouter()
router.register("postStoraged", viewset=postStoragedViewSet, basename="postStoraged")
router.register("postlist", viewset=postlistViewSet, basename="postlist")

urlpatterns = [
    path("", include((router.urls, app_name), namespace="userdetail")),
]
