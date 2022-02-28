from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        (1, 'user'),
        (2, 'moderator'),
        (3, 'admin'),
    )
    email = models.EmailField(
        verbose_name='электронная почта',
        max_length=254,
        unique=True,
        required=True,
    )
    first_name = models.CharField(
        verbose_name='имя пользователя', max_length=150, blank=True,
    )
    bio = models.TextField(verbose_name='биография', blank=True)
    role = models.CharField(
        verbose_name='роль', max_length=1, choices=ROLE_CHOICES, default=1,
    )
    REQUIRED_FIELDS = ['username', 'email']
