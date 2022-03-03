from django.db import models
from django.core.validators import RegexValidator

from api_yamdb.settings import REGEX_CATEGORY
from users.models import User


class CATEGORIES(models.Model):
    CATEGORY_VALIDATOR = RegexValidator(REGEX_CATEGORY,
                                        'Введены неправильные знаки!')
    name = models.CharField(required=True, max_length=256, unique=True,
                            verbose_name='Категория')
    slug = models.SlugField(unique=True, max_length=50,
                            validators=(CATEGORY_VALIDATOR,),
                            required=True)

    def __str__(self):
        return self.name


class GENRES(models.Model):
    name = models.CharField(required=False, verbose_name='Жанр')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class TITLES(models.Model):
    name = models.CharField(required=True,
                            verbose_name='Название Произведения')
    year = models.IntegerField(required=True)
    description = models.TextField(
        max_length=200,
        blank=True
    )
    genre = models.ManyToManyField(
        GENRES,
        required=True,
        related_name='genre',
        on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        CATEGORIES,
        on_delete=models.SET_NULL,
        required=True,
        related_name='category'
    )

    def __str__(self):
        return self.name


class Score(models.Model):
    """"""
    title = models.ForeignKey(
        TITLES,
        on_delete=models.CASCADE(),
        verbose_name='name of title',
        related_name='score'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
        related_name='author_posts')

class Review(models.Model):
    """"""
    title = models.ForeignKey(
        TITLES,
        on_delete=models.CASCADE(),
        verbose_name='name of title',
        related_name='review'
    )
    text = models.CharField('review of title', required=True,
                            verbose_name='Название Произведения')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
        related_name='author_posts')
    score =