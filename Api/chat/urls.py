from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


app_name = "chat"

router = DefaultRouter()
router.register("chats", viewset=ChatViewSet, basename="chats")
router.register("getUser", viewset=getUserViewSet, basename="getUser")
router.register("getPrevious", viewset=getPreviousViewSet, basename="getPrevious")


urlpatterns = [
    path("", include((router.urls, app_name), namespace="chat")),
]
