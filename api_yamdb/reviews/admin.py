from django.conf import settings
from django.contrib import admin

from .models import Comment, Title, Review


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Сustom admin panel for title."""
    list_display = (
        'pk',
        'name',
        'year',
        'description',
    )
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Custom admin panel for Review."""
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Custom admin panel for comment."""
    list_display = (
        'pk',
        'review_id',
        'text',
        'author',
        'pub_date'
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY
