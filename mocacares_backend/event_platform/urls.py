from django.conf.urls import include, url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^api/event/eventDetail', views.get_event),

    url(r'^api/event/commentAdd', views.post_comment),
]
