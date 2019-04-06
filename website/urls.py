from django.conf.urls import url
from . import views

app_name = 'website'

urlpatterns = [
    # /general/
    #url('^$', views.LogInView.as_view(), name='index'),
    # /general/login/
    #url('^login$', views.LogInView.as_view(), name='login'),
    # /general/register/
    url(r'^$', views.register, name='register'),
]
