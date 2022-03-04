from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.shortcuts import get_object_or_404

from review.models import Comment, Review, TITLES, User


class ReviewGetSerializer(serializers.ModelSerializer):
    """Serializer for reiding and get AVG."""
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())
    score = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def get_score(self, obj):
        title_id = self.context.get('view').kwargs.get('title_id')
        av = Review.objects.filter(title=title_id).aggregate(
            Avg('score')).get('score__avg')
        return av


class ReviewPostSerializer(serializers.ModelSerializer):
    """Serializer for writing."""
    author = SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if 1 <= value <= 10:
            return value
        raise serializers.ValidationError('Значение должно быть в интервале от 1 до 10!')

    def create(self, validated_data):
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(TITLES, pk=title_id)
        author = self.context['request'].user
        author = get_object_or_404(User, username=author)
        review = Review.objects.create(**validated_data,
                                       title=title,
                                       author=author)
        return review


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""
    author = SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment

    def create(self, validated_data):
        review_id = self.context.get('view').kwargs.get('review_id')
        author = self.context['request'].user
        review_id = get_object_or_404(Review, pk=review_id)
        comment = Comment.objects.create(**validated_data,
                                         review_id=review_id,
                                         author=author)
        return comment
