from django.shortcuts import render,\
    get_object_or_404

from django.views.decorators.http import require_http_methods, \
    require_safe
from .models import *
from .forms import *

import redis
from django.conf import settings

from django.core.paginator import Paginator,\
    PageNotAnInteger,\
    EmptyPage

from django.core.mail import send_mail

from taggit.models import Tag
from django.db.models import Count

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)

# Create your views here.


@require_http_methods(['GET'])
def shop(request, tag_slug=None):
    items = Book.objects.order_by('item_date_updated').reverse()

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        items = items.filter(tags__in=[tag])

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
        'tag': tag,
    }
    return render(request, 'index.html', context)


@require_http_methods(['GET', 'POST'])
def book_detail(request, book_slug, author_slug):
    book = get_object_or_404(Book, slug=book_slug)
    author = get_object_or_404(Author, slug=author_slug)

    comments = book.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.book = book
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    book_tags_ids = book.tags.values_list('id', flat=True)
    similar_books = Book.objects.filter(tags__in=book_tags_ids)\
        .exclude(id=book.id)
    similar_books = similar_books.annotate(same_tags=Count('tags')) \
        .order_by('-same_tags')[:4]

    context = {
        'book': book,
        'author': author,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_books': similar_books,
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


@require_safe
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