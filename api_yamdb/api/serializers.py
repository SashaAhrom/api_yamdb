from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from review.models import Comment, Review


class Score(serializers.Field):
    # При чтении данных ничего не меняем - просто возвращаем как есть
    def to_representation(self, value):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        return title.review.all().aggregate(Avg('score'))

    def to_internal_value(self, data):
        if 1 <= data <= 10:
            return data
        raise serializers.ValidationError('Value must be between 1 and 10.')


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username')
    score = Score()

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
