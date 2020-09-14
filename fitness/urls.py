from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.steps_home, name='steps'),
]