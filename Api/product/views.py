from django.shortcuts import render
from rest_framework import viewsets
from .models import product, product_category
from .serializer import productSerializer, productCategorySerializer
from userprofile.models import bodyProfile, profile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.


class productViewSet(viewsets.ModelViewSet):
    queryset = product.objects.all()
    serializer_class = productSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['product_category__category_name', 'exchaged']
    search_fields = ['product_title', 'product_description', 'product_category__category_name']

    ordering_fields = ['product_point', 'exchaged']

class productCategoryViewSet(viewsets.ModelViewSet):
    queryset = product_category.objects.all()
    serializer_class = productCategorySerializer


class productRecommendationViewSet(viewsets.ModelViewSet):
    queryset = product.objects.all()
    serializer_class = productSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['product_category__category_name', 'exchaged']
    search_fields = ['product_title', 'product_description', 'product_category__category_name']

    ordering_fields = ['product_point', 'exchaged']

    """
    再很之前有說過要依照使用者的資料來推薦商品，這邊就是要依照使用者的資料來推薦商品
    但目前都沒有拿出來說，所以就先將這功能註解掉，但還是可以運行，如果有需要就可以拿出來使用
    """

    # def get_queryset(self):
    #     user = self.request.user
    #     family_planning = bodyProfile.objects.get(user=user).family_planning
    #     expecting = bodyProfile.objects.get(user=user).expecting
    #     print(family_planning, expecting)
    #     queryset = product.objects.all()
    #     category = self.request.query_params.get('category', None)
    #     if category is not None:
    #         queryset = queryset.filter(product_category__category_name=category)
    #     return queryset
    #
    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['user'] = self.request.user
    #     return context