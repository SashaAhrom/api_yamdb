from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator)

User = get_user_model()


class Review(models.Model):
    """Review model."""
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Title',
        related_name='review')
    text = models.TextField('review')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
        related_name='author_review')
    score = models.IntegerField(verbose_name='score',
                                validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField('time of writing', auto_now_add=True)

    class Meta:
        verbose_name = 'review'
        db_table = 'reviews for title'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Add commets to review."""
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='review',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author name',
        related_name='author_comments')
    text = models.TextField('coment', help_text='Введите текст коментария')
    pub_date = models.DateTimeField('time of writing', auto_now_add=True)

    class Meta:
        verbose_name = 'comments'
        db_table = 'users comments'

    def __str__(self):
        return self.text[:15]
