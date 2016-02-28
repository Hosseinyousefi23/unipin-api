from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'(?P<id>[0-9]+)', views.show_post, name='event_show_post')
]
