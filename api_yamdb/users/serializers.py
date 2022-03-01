from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):

    username = serializers.RegexField(regex=r'^[\w.@+-]+\z')
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=User.ROLES_CHOICES)

    class Meta:

        model = User
        fields = (
            'username', 'first_name', 'last_name', 'bio', 'email', 'role',
        )
        validators = (
            UniqueValidator(
                queryset=User.objects.all(),
                message='Такое имя уже занято!',
            ),
        )
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Email {email} уже занят!',
            )

    def validate_username(self, username):

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Пользователь с именем {username} уже зарегистрирован!'
            )
        if username == 'me':
            raise serializers.ValidationError(
                'Данное имя пользователя недопустимо.'
                'Пожалуйста, выберите другое имя пользователя.'
            )

class ConfirmationCodeSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate_email(self, email):

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Почтовый адрес {email} уже зарегистрирован!',
            )
        return email

    def validate_username(self, username):

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Пользователь с именем {username} уже зарегистрирован!'
            )
        if username == 'me':
            raise serializers.ValidationError(
                'Данное имя пользователя недопустимо.'
                'Пожалуйста, выберите другое имя пользователя.'
            )
