from django.contrib import admin
from .models import BookInfo, HeroInfo


@admin.register(BookInfo)
class BookInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(HeroInfo)
class HeroInfoAdmin(admin.ModelAdmin):
    pass
