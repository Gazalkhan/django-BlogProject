from django.conf.urls import url
from . import views
from django.views.decorators.cache import cache_page

app_name = 'articles'

urlpatterns = [
    url(r'^$', views.article_list, name="list"),
    url(r'^create/$', views.article_create, name="create"),
    url(r'^(?P<slug>[\w-]+)/$', views.article_detail, name="detail"),
    url(r'^(?P<slug>[\w-]+)/comment/$', views.article_add_comment_to_post, name='add_comment_to_post'),
    url(r'^(?P<slug>[\w-]+)/$', views.cache_view, name='cache')

]
