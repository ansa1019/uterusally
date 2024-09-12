from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "user_auth"

router = DefaultRouter()
router.register("register", viewset=RegisterationViewSet, basename="register")
router.register("user_config", viewset=UserViewSet, basename="change_password")
# router.register(
#     r"mail_verify/(?P<username>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+)/$",
#     viewset=MailVerifyViewSet,
#     basename="mail_verify",
# )

urlpatterns = [
    path("", include((router.urls, app_name), namespace="user_auth")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    re_path(
        r"mail_verify/(?P<username>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+)/$",
        MailVerifyViewSet.as_view({"get": "list"}),
        name="mail_verify",
    ),
    re_path(
        r"forget_password/(?P<username>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+)/$",
        ForgetPasswordViewSet.as_view({"post": "create"}),
        name="forget_password",
    ),
]
