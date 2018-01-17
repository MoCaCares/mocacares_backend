from django.conf.urls import include, url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^api/event/eventDetail', views.get_event),

    url(r'^api/event/commentAdd', views.post_comment),

    url(r'^api/event/eventList', views.get_events),
    
    url(r'^api/event/eventRecommend', views.get_recommended_events),

    url(r'^api/event/eventTypeList', views.get_event_types),

    url(r'^api/event/commentList', views.get_comments),

    url(r'^api/event/eventBook', views.book_event),

    url(r'^api/event/eventMyBook', views.get_booked_events),

    url(r'^api/event/eventMyPublish', views.get_published_events),

    url(r'^api/users/userInfoGet', views.get_user_info),
    
    url(r'^api/users/userSpace', views.get_user_space),
    
    url(r'^api/login/register', views.user_register),

    url(r'^api/login/login', views.user_login),

    url(r'^api/public/feedback', views.post_feedback),

    url(r'^api/chat/getNoRead', views.get_noreads),
]
