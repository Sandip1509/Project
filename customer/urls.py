from django.conf.urls import url
from . import views
app_name = 'customer'


urlpatterns = [
    # /customer/
    url(r'^$', views.home , name='home'),
]