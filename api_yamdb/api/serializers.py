import datetime as dt

from django.db.models import Avg
from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from api_yamdb.settings import REGEX_CATEGORY
from users.models import User
from reviews.models import Categories, Comment, Genres, Review, Title


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
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('count', 'id', 'name', 'year',
                  'description', 'rating', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        title_id = self.context.get('view').kwargs.get('pk')
        print(self.context.get('view').kwargs)
        av = Review.objects.filter(title=title_id).aggregate(
            Avg('score')).get('score__avg')
        return av


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Categories.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        year = dt.datetime.today().year
        if value > year:
            raise serializers.ValidationError('Не правильно указан год')
        return value


class ReviewGetSerializer(serializers.ModelSerializer):
    """Serializer for reiding and get AVG."""
    author = SlugRelatedField(
        read_only=True,
        slug_field='username')


    class Meta:
        fields = ('id', 'text', 'author',  'score', 'pub_date')
        model = Review


class CurrentTitleDefault:
    """
    May be applied as a `default=...` value on a serializer field.
    Returns the title_id.
    """
    requires_context = True

    def __call__(self, serializer_field):
        print(serializer_field.context.get('view').kwargs.get('title_id'))
        return serializer_field.context.get('view').kwargs.get('title_id')


class TypeDefault(object):
    def set_context(self, serializer_field):
        view = serializer_field.context['view']

        self.type = view.kwargs['title_id'].upper()

    def __call__(self):
        return self.type

class ReviewPostSerializer(serializers.ModelSerializer):
    """Serializer for writing."""
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())
    title = serializers.HiddenField(default=TypeDefault())

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if 1 <= value <= 10:
            return value
        raise serializers.ValidationError('Значение должно быть в интервале от 1 до 10!')

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
