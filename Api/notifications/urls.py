from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


app_name = "notifications"

router = DefaultRouter()
router.register("notifications", viewset=notificationsView, basename="notifications")
router.register("getNotifications", viewset=getNotificationsView, basename="getNotifications")

urlpatterns = [
    path("", include((router.urls, app_name), namespace="notifications")),
]
