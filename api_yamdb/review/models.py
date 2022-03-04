from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

from api_yamdb.settings import REGEX_CATEGORY
from users.models import User


class CATEGORIES(models.Model):
    CATEGORY_VALIDATOR = RegexValidator(REGEX_CATEGORY,
                                        'Введены неправильные знаки!')
    name = models.CharField(max_length=256, unique=True,
                            verbose_name='Категория')
    slug = models.SlugField(unique=True, max_length=50,
                            validators=(CATEGORY_VALIDATOR,))

    def __str__(self):
        return self.name


class GENRES(models.Model):
    name = models.CharField(max_length=256, verbose_name='Жанр')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class TITLES(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название Произведения')
    year = models.IntegerField()
    description = models.TextField(
        max_length=200,
        blank=True
    )
    genre = models.ManyToManyField(
        GENRES,
        related_name='genre',
        blank=True,
    )
    category = models.ForeignKey(
        CATEGORIES,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    """Reviews for titles."""
    title = models.ForeignKey(
        TITLES,
        on_delete=models.CASCADE,
        verbose_name='name of title',
        related_name='review_title'
    )
    text = models.TextField('review of title')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
        related_name='author_posts')
    score = models.SmallIntegerField(verbose_name='score',
                                     validators=[MaxValueValidator(10),
                                                 MinValueValidator(1)])
    pub_date = models.DateTimeField('year of writing', auto_now_add=True)

    class Meta:
        db_table = 'review for title'
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique score')
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Comments on reviews."""
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='name of review',
        related_name='review_comment'
    )
    text = models.TextField('comment on review')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
        related_name='author_comment')
    pub_date = models.DateTimeField('year of writing', auto_now_add=True)

    class Meta:
        db_table = 'comment on review'

    def __str__(self):
        return self.text[:15]