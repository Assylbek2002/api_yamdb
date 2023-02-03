import django_filters
from .models import Title, Category, Genre


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.ModelMultipleChoiceFilter(
        field_name='genre__slug',
        to_field_name='slug',
        queryset=Genre.objects.all()
    )
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category__slug',
        to_field_name='slug',
        lookup_expr='iexact',
        queryset=Category.objects.all()
    )
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    year = django_filters.NumberFilter(
        field_name='year', lookup_expr='iexact'
    )

    class Meta:
        fields = ('genre', 'category', 'name', 'year')
        model = Title
