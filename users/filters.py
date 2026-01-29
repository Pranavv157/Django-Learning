import django_filters
from .models import UserProfile


class UserFilter(django_filters.FilterSet):

    # contains search (LIKE %text%)
    name = django_filters.CharFilter(lookup_expr="icontains")

    # exact match
    email = django_filters.CharFilter(lookup_expr="exact")

    # boolean filter
    is_active = django_filters.BooleanFilter()

    # id >= value
    min_id = django_filters.NumberFilter(field_name="id", lookup_expr="gte")

    # id <= value
    max_id = django_filters.NumberFilter(field_name="id", lookup_expr="lte")


    class Meta:
        model = UserProfile
        fields = []
