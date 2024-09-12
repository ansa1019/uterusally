from django_filters import rest_framework
from .models import contentPost


class contentPostFilter(rest_framework.FilterSet):
    username = rest_framework.CharFilter(field_name='author__username', lookup_expr='icontains')
    title = rest_framework.CharFilter(field_name='title', lookup_expr='icontains')
    body = rest_framework.CharFilter(field_name='body', lookup_expr='icontains')

    class Meta:
        model = contentPost
        fields = ['username', 'title', 'body', ]

