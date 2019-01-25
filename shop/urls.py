from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.shop, name='shop'),
    # path('archive/2018', views.archive, name='archive'),
    path('<slug:author_slug>', views.author_detail, name='author_detail'),
    path('<slug:author_slug>/<slug:book_slug>', views.book_detail, name='book_detail'),

]

