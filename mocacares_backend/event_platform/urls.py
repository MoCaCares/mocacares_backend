from django.conf.urls import include, url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^api/event/eventDetail', views.get_event),

    url(r'^api/event/commentAdd', views.post_comment),

    url(r'^api/event/eventList', views.get_events),
    
    url(r'^api/event/eventRecommend', views.get_recommended_events),

    url(r'^api/event/eventTypeList', views.get_event_types),

    url(r'^api/users/userInfoGet', views.get_user),
    
    url(r'^api/login/login', views.user_login),

    url(r'^api/public/feedback', views.post_feedback),
]
