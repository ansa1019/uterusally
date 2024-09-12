import django_filters
from rest_framework import filters
from userprofile.models import personal_calendar


class personalCalendarFilter(filters.BaseFilterBackend):
    today = django_filters.DateFilter(field_name='date', lookup_expr='gte')

    class Meta:
        model = personal_calendar
        fields = ['today', 'date']

    def filter_queryset(self, request, queryset, view):
        print(request.query_params.get('today', None))
        return queryset.filter(date__gte=request.query_params.get('today', None)[::-1])


# class recommendationFilter(filters.BaseFilterBackend):
#     today = django_filters.DateFilter(field_name='date', lookup_expr='gte')
#
#     class Meta:
#         model = personal_calendar
#         fields = ['today', 'date']
#
#     def filter_queryset(self, request, queryset, view):
#         print(request.query_params.get('today', None))
#         return queryset.filter(date__gte=request.query_params.get('today', None)[::-1])