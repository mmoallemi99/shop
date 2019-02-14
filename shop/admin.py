from django.contrib import admin
from .models import *


@admin.decorators.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'item_date_published',
                    'book_date_published',
                    'gen_display',
                    'auth_display',)
    list_filter = ('item_date_published',
                   'book_date_published',)
    prepopulated_fields = {'slug': ('title',)}

    def gen_display(self, obj):
        return ", ".join([gen.name for gen in obj.genre.all()[:3]])

    gen_display.short_description = "Genres"

    def auth_display(self, obj):
        return " ".join([obj.author.name, obj.author.f_name])

    auth_display.short_description = "Author"


@admin.decorators.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.decorators.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', 'f_name')}
    fields = [
        'name',
        'f_name',
        'slug',
        ('date_of_birth', 'date_of_death'),
        ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'book', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
