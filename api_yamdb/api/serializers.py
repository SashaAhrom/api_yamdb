from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from review.models import Review, Score


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='first_name')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
