from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET
from .models import *

# Create your views here.


@require_http_methods(['GET'])
def shop(request):
    items = Book.objects.order_by('item_date_updated').reverse()[:5]
    context = {
        'items': items,
    }
    return render(request, 'index.html', context)


@require_GET
def book_detail(request, book_slug, author_slug):
    book = get_object_or_404(Book, slug=book_slug)
    author = get_object_or_404(Author, slug=author_slug)
    context = {
        'book': book,
        'author': author,
    }
    return render(request, 'book.html', context)


@require_GET
def author_detail(request, author_slug):
    author = get_object_or_404(Author, slug=author_slug)
    context = {
        'author': author,
    }
    return render(request, 'author.html', context)

"""
@require_GET
def archive(request):
    items = Book.objects.order_by('item_date_updated').reverse()
    context = {
        'items': items,
    }
    return render(request, 'archive.html', context)

"""