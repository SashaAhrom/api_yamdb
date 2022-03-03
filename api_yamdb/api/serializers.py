from django.shortcuts import get_object_or_404
from rest_framework import serializers

from yamdb.models import CATEGORIES, GENRES, TITLES


class CATEGORIESSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True,
                                     source='CATEGORIES__name.count')

    class Meta:
        model = CATEGORIES
        fields = ('count', ['name', 'slug'])


class GENRESSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True,
                                     source='GENRES__slug.count')
    class Meta:
        model = GENRES
        exlude = ('id')


class TITLESSerializer(serializers.ModelSerializer):

    class Meta:
        model = TITLES
        exlude = ('id')
