from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^steps/', views.steps, name='steps'),
    url(r'^calories/', views.calories, name='calories'),
]