from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    productViewSet, productCategoryViewSet, productRecommendationViewSet,
)


app_name = 'product'

router = DefaultRouter()
router.register('product', viewset=productViewSet, basename='product')
router.register('productCategory', viewset=productCategoryViewSet, basename='productCategory')
router.register('productRecommend', viewset=productRecommendationViewSet, basename='productRecommend')



urlpatterns = [
    path('', include((router.urls, app_name), namespace='product')),
]

