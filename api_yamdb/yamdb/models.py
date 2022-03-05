
import datetime as dt

from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator

from api_yamdb.settings import REGEX_CATEGORY


class Categories(models.Model):
    CATEGORY_VALIDATOR = RegexValidator(REGEX_CATEGORY,
                                        'Введены неправильные знаки!')
    name = models.CharField(max_length=256,
                            verbose_name='Категория')
    slug = models.SlugField(max_length=50,
                            validators=(CATEGORY_VALIDATOR,),
                            )

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=30,
                            verbose_name='Жанр')
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название Произведения')
    year = models.IntegerField(
        validators=[MaxValueValidator(dt.datetime.now().year)])
    description = models.TextField(
        max_length=200,
        blank=True
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='genre',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='category',
        null=True
    )

    def __str__(self):
        return self.name
