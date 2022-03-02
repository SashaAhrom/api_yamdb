from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueValidator

from .models import User


class AdminSerializer(serializers.ModelSerializer):
    
    username = serializers.RegexField(regex=r'^[\w.@+-]+')
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=User.ROLES_CHOICES, default=User.USER, initial=User.USER,
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Данное имя пользователя уже используется!'
            )
        if username == 'me':
            raise serializers.ValidationError(
                'Данное имя пользователя недопустимо.'
                'Пожалуйста, выберите другое имя пользователя.',
            )
        return username
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Данная электронная почта уже используется!',
            )
        return email


class UserSerializer(AdminSerializer):
    """Serializer for UserViewSet."""

    username = serializers.RegexField(regex=r'^[\w.@+-]+')
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=User.ROLES_CHOICES, default=User.USER, read_only=True,
    )

    # class Meta:

    #     model = User
    #     fields = (
    #         'username', 'email', 'first_name', 'last_name', 'bio', 'role',
    #     )

    # def validate_username(self, username):
    #     """Validates username field."""
    #     if username == 'me':
    #         raise serializers.ValidationError(
    #             'Данное имя пользователя недопустимо.'
    #             'Пожалуйста, выберите другое имя пользователя.',
    #         )
    #     return username
    
    # def validate_email(self, email):
    #     """Validates email field."""
    #     if User.objects.filter(email=email).exists():
    #         raise serializers.ValidationError(
    #             'Данная электронная почта уже используется!',
    #         )
    #     return email


    


class ConfirmationCodeSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Данная электронная почта уже используется!',
            )
        return email


    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Данное имя пользователя уже занято!',
            )
        if username == 'me':
            raise serializers.ValidationError(
                'Данное имя пользователя недопустимо.'
                'Пожалуйста, выберите другое имя пользователя.',
            )
        return username


class ValidationError404(APIException):
    status_code = status.HTTP_404_NOT_FOUND


class JwtTokenSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    confirmation_code = serializers.UUIDField(required=True)

    def is_valid(self, raise_exception=False):
        msg = 'Пользователя с такими данными не найдено!'
        try:
            return super().is_valid(raise_exception)
        except serializers.ValidationError as e:
            if str(e) == msg:
                raise ValidationError404(detail=e.detail)
            raise serializers.ValidationError(detail=e.detail)


    def validate(self, attrs):
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
        if not User.objects.filter(username=username).exists():
            raise ValidationError404(
                'Пользователя с такими данными не найдено!',
            )
        return username
    
    def validate_confirmation_code(self, confirmation_code):
        if not User.objects.filter(
            confirmation_code=confirmation_code,
        ).exists():
            raise serializers.ValidationError(
                'Код подтвеждения не найден!',
            )
        return confirmation_code
        
