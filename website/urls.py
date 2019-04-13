from django.conf.urls import url
from . import views

app_name = 'website'

urlpatterns = [
    # /general/
    #url('^$', views.LogInView.as_view(), name='index'),
    # /general/login/
    #url('^login$', views.LogInView.as_view(), name='login'),
    # /general/register/
    url(r'^login/$', views.user_login, name='login'),
    url(r'^signup/$', views.register , name='signup'),
    url(r'^logout/$',views.user_logout,name='logout'),
]
