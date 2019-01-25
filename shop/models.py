from django.db import models
from django.utils import timezone


class Genre(models.Model):
    name = models.CharField('Genre', max_length=100, help_text="Book Genre (e.g. Sci-Fi, Programming etc.")

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100, help_text="Author Name")
    f_name = models.CharField('family name', max_length=100, help_text="Author Family Name")
    slug = models.SlugField(max_length=50, help_text="Author Link")
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def __str__(self):
        return "{0} {1}".format(self.name, self.f_name)

    def auth_slug(self):
        return "{0}-{1}".format(self.name, self.f_name)


class Book(models.Model):
    title = models.CharField(max_length=150, help_text="Book Title")
    slug = models.SlugField(max_length=50, help_text="Book Link")
    description = models.TextField(max_length=1500, help_text="Book Short Description")
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, help_text="Select Author For This Book", null=True)
    genre = models.ManyToManyField(Genre, help_text="Select Genres For This Book")
    stock_available = models.IntegerField(default=5)
    img = models.ImageField(upload_to='pics', null=True, blank=True)
    item_date_published = models.DateTimeField(default=timezone.now)
    item_date_updated = models.DateTimeField(auto_now=True)
    book_date_published = models.DateField()

    def __str__(self):
        return "{0} By".format(self.title)



