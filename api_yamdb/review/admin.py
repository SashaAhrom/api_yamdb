from django.conf import settings
from django.contrib import admin

from .models import Comment, TITLES, Review


@admin.register(TITLES)
class TITLESAdmin(admin.ModelAdmin):
    """Сustom admin panel for Post."""
    list_display = (
        'pk',
        'name',
        'year',
        'category',
    )


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
