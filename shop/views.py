from django.shortcuts import render,\
    get_object_or_404

from django.views.decorators.http import require_http_methods,\
    require_GET

from .models import *
from .forms import *

import redis
from django.conf import settings

from django.core.paginator import Paginator,\
    PageNotAnInteger,\
    EmptyPage

from django.core.mail import send_mail

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)

# Create your views here.


@require_http_methods(['GET'])
def shop(request):
    items = Book.objects.order_by('item_date_updated').reverse()
    paginator = Paginator(items, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'posts': posts,
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


def book_share(request, book_slug, author_slug):
    book = get_object_or_404(Book, slug=book_slug)
    author = get_object_or_404(Author, slug=author_slug)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            book_url = request.build_absolute_uri()[:-6]
            subject = '{} ({}) recommends you buying "{}"'.format(cd['name'],
                                                                  cd['email'],
                                                                  book.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(book.title,
                                                                    book_url,
                                                                    cd['name'],
                                                                    cd['comments'])
            send_mail(subject, message, 'admin@shop.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        'book': book,
        'form': form,
        'sent': sent,
    }
    return render(request, 'share.html', context)


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