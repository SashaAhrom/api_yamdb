from django_filters import rest_framework as filters

from .models import Titles


class TitlesFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__slug',
                                  lookup_expr='exact')
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='exact')
    year = filters.NumberFilter(field_name='year', lookup_expr='exact')

    class Meta:
        model = Titles
        fields = ('name', 'category', 'genre', 'year')
