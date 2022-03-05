from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from review.models import Comment, Review, TITLES
from users.models import User


class AdminSerializer(serializers.ModelSerializer):
    """Serializer for admin users for UserViewSet."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+',
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    role = serializers.ChoiceField(
        choices=User.ROLES_CHOICES, default=User.USER, initial=User.USER,
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def validate_username(self, username):
        """Checks if given username is forbidden for registration."""
        if username == 'me':
            raise serializers.ValidationError(
                'Данное имя пользователя недопустимо.'
                'Пожалуйста, выберите другое имя пользователя.',
            )
        return username


class UserSerializer(AdminSerializer):
    """Serializer for users/me view."""

    role = serializers.ChoiceField(
        choices=User.ROLES_CHOICES, default=User.USER, read_only=True,
    )


class ConfirmationCodeSerializer(serializers.Serializer):
    """Serializer for handling user signup."""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+',
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    def validate_username(self, username):
        """Checks if given username is forbidden for registration."""
        if username == 'me':
            raise serializers.ValidationError(
                'Данное имя пользователя недопустимо.'
                'Пожалуйста, выберите другое имя пользователя.',
            )
        return username


class ValidationError404(APIException):
    """Custom error for returning NOT_FOUND response."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Пользователя с такими данными не найдено!'


class JwtTokenSerializer(serializers.Serializer):
    """Serializer for handling jwt token aquisition."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.UUIDField(required=True)

    def is_valid(self, raise_exception=False):
        """Custom check if validation error with specific message is raised."""
        msg = 'Пользователя с такими данными не найдено!'
        try:
            return super().is_valid(raise_exception)
        except serializers.ValidationError as error:
            if str(error) == msg:
                raise ValidationError404(detail=error.detail)
            raise serializers.ValidationError(detail=error.detail)

    def validate(self, attrs):
        """Check if confirmation code for given username is valid."""
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')
        if not User.objects.filter(
                username=username, confirmation_code=confirmation_code,
        ).exists():
            raise ValidationError404(
                'Пользователя с такими данными не найдено!',
            )
        return attrs

    def validate_username(self, username):
        """Checks if user with given username exists."""
        if not User.objects.filter(username=username).exists():
            raise ValidationError404(
                'Пользователя с такими данными не найдено!',
            )
        return username


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


class CurrentTitleDefault:
    """
    May be applied as a `default=...` value on a serializer field.
    Returns the title_id.
    """
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context.get('view').kwargs.get('title_id')


class ReviewPostSerializer(serializers.ModelSerializer):
    """Serializer for writing."""
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())
    title = serializers.HiddenField(write_only=True, default=CurrentTitleDefault())

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
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

    validators = (
        UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=('title', 'author'),
            message='You can only write one review.'
        ),
    )


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
