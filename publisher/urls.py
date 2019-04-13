from django.conf.urls import url
from . import views

app_name = 'publisher'


urlpatterns = [
    # /publisher/
    url(r'^$', views.HomeView.as_view(), name='home'),

    # /publisher/album/add/
    url(r'^add/$', views.EBookCreate.as_view(), name='ebook-add'),

    url(r'^(?P<pk>[0-9]+)/chapters/$', views.createChapters, name='chapter-add'),

    url(r'^(?P<pk>[0-9]+)/chaptersdetails/$', views.ChapterDetailView.as_view(), name='chapter-details'),

    url(r'publisher/(?P<pk>[0-9]+)/chaptersdelete/$', views.ChapterDelete.as_view(), name='chapter-delete'),


    # /publisher/album/2/
    url(r'publisher/(?P<pk>[0-9]+)/$', views.EBookUpdate.as_view(), name='ebook-update'),

    # /publisher/album/2/delete/
    url(r'publisher/(?P<pk>[0-9]+)/delete/$', views.EBookDelete.as_view(), name='ebook-delete'),
]