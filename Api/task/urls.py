from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import taskViewSet, taskRecordViewSet


app_name = 'task'

router = DefaultRouter()
router.register('task', viewset=taskViewSet, basename='task')
router.register('taskRecord', viewset=taskRecordViewSet, basename='taskRecord')


urlpatterns = [
    path('', include((router.urls, app_name), namespace='point')),
]

