from django.contrib import admin
from yamdb.models import Categories, Genres, Titles


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description')
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


admin.site.register(Titles, TitlesAdmin)
admin.site.register(Categories)
admin.site.register(Genres)
