import datetime as dt

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from yamdb.models import Categories, Genres, Titles
from api_yamdb.settings import REGEX_CATEGORY


class CategoriesSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True,
                                     source='categories.count')
    slug = serializers.RegexField(regex=REGEX_CATEGORY,
                                  validators=[UniqueValidator(
                                      queryset=Categories.objects.all())])

    class Meta:
        model = Categories
        lookup_field = 'slug'
        fields = ('count', 'name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True,
                                     source='genres.count')
    slug = serializers.CharField(validators=[UniqueValidator(
        queryset=Genres.objects.all())])

    class Meta:
        model = Genres
        fields = ('count', 'name', 'slug')


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    count = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('count', 'id', 'name', 'year',
                  'description', 'genre', 'category')
        model = Titles


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Categories.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Titles

    def validate_year(self, value):
        year = dt.datetime.today().year
        if value > year:
            raise serializers.ValidationError('Не правильно указан год')
        return value
