from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.file_upload_form, name='upload'),
]