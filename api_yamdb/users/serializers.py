from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import User


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
