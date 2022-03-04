from django.conf import settings
from django.contrib import admin

from .models import TITLES, Review


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
    """Сustom admin panel for Post."""
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
