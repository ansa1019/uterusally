from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


app_name = 'userprofile'

router = DefaultRouter()
router.register('profile', viewset=profileViewSet, basename='profile')
router.register('bodyProfile', viewset=bodyProfileViewSet, basename='bodyProfile')
router.register('subscribe', viewset=subscribeViewSet, basename='subscribe')
router.register('personalCalendar', viewset=personalCalendarViewSet, basename='personalCalendar')
router.register('subPersonalCalendar', viewset=subPersonalCalendarViewSet, basename='subPersonalCalendar')
router.register('menstrual', viewset=menstrualViewSet, basename='menstrual')
router.register('subTopic', viewset=subTopicViewSet, basename='subTopic')
router.register('recommendUser', viewset=recommendUserViewSet, basename='recommendUser')
router.register('subscribeHashtag', viewset=subscribeHashtagViewSet, basename='subscribeHashtag')

urlpatterns = [
    path('', include((router.urls, app_name), namespace='userprofile')),
]

