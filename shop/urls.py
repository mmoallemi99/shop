from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('tag/<slug:tag_slug>/',
         views.shop,
         name='book_list_by_tag'),
    path('<slug:author_slug>',
         views.author_detail,
         name='author_detail'),
    path('<slug:author_slug>/<slug:book_slug>/',
         views.book_detail,
         name='book_detail'),
    path('<slug:author_slug>/<slug:book_slug>/share/',
         views.book_share,
         name='book_share'),

]

