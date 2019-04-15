from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'products'

urlpatterns = [
    url(r'^$', views.product_list, name='product-list'),
    url(r'^(?P<pk>[0-9]+)/chaptersdetails/$', views.chapter_details, name='chapterdetails'),

]
