from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'publisher'


urlpatterns = [
    # /publisher/
    url(r'^$', views.home, name='home'),

    # /publisher/album/add/
    url(r'^add/$', login_required(views.EBookCreate.as_view()), name='ebook-add'),

    url(r'^(?P<pk>[0-9]+)/chapters/$', views.createChapters, name='chapter-add'),

    url(r'^(?P<pk>[0-9]+)/chaptersdetails/$', login_required(views.ChapterDetailView.as_view()), name='chapter-details'),

    url(r'publisher/(?P<pk>[0-9]+)/chaptersdelete/$', login_required(views.ChapterDelete.as_view()), name='chapter-delete'),


    # /publisher/album/2/
    url(r'publisher/(?P<pk>[0-9]+)/$', login_required(views.EBookUpdate.as_view()), name='ebook-update'),

    # /publisher/album/2/delete/
    url(r'publisher/(?P<pk>[0-9]+)/delete/$', login_required(views.EBookDelete.as_view()), name='ebook-delete'),
]