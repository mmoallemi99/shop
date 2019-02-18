from django import template
from ..models import Book

from django.db.models import Count

register = template.Library()


@register.simple_tag()
def get_most_commented_books(count=5):
    books = Book.objects.annotate(total_comments=Count('comments')).order_by('-total_comments', '-item_date_updated')[:count]
    return books
