from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import pointView, giftView, exchangeProductView, systemPointView


app_name = "point"

router = DefaultRouter()
router.register("userPoint", viewset=pointView, basename="userPoint")
router.register("exchange", viewset=exchangeProductView, basename="exchange")
router.register("gift", viewset=giftView, basename="gift")
router.register("systemPoint", viewset=systemPointView, basename="systemPoint")

urlpatterns = [
    path("", include((router.urls, app_name), namespace="point")),
]
