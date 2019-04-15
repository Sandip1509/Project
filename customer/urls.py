from django.conf.urls import url
from . import views


app_name = 'customer'
urlpatterns = [
    # /customer/
     url(r'^$', views.home , name='home'),
     url(r'^buy/$', views.Buy , name='buy'),
     # url(r'^(?P<pk>[0-9]+)/orderdelete/$', views.OrderDelete.as_view(), name='orderDelete'),
     url(r'^search/$', views.search , name='search'),
     url(r'^(?P<pk>[0-9]+)/OrderItemDelete/$',views.OrderItemDelete.as_view(),name='OrderItemDelete'),

    # url(r'^(?P<pk>[0-9]+)/chaptersdetails/$', views.ChapterDetailView.as_view(), name='chapter-details'),

    # url(r'^cart/$', views.AddToCart.as_view(), name='cart-add'),

]