from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


app_name = "blacklist"

router = DefaultRouter()
router.register("status", viewset=StatusViewSet, basename="status")
router.register("blacklist", viewset=blacklistViewSet, basename="blacklist")
router.register("getBlacklist", viewset=getBlacklistViewSet, basename="getBlacklist")
router.register("getBanlist", viewset=getBanlistViewSet, basename="getBanlist")

urlpatterns = [
    path("", include((router.urls, app_name), namespace="blacklist")),
]
