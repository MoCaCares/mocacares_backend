from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views


urlpatterns = [
    url(r'^api/event/eventDetail$', views.get_event),

    url(r'^api/event/commentAdd$', views.post_comment),

    url(r'^api/event/eventDel$', views.delete_event),

    url(r'^api/event/eventAdd$', views.add_event),

    url(r'^api/event/eventList$', views.get_events),

    url(r'^api/event/eventRecommend$', views.get_recommended_events),

    url(r'^api/event/eventTypeList$', views.get_event_types),

    url(r'^api/event/commentList$', views.get_comments),

    url(r'^api/event/commentMy$', views.get_my_comments),

    url(r'^api/public/systemConfig$', views.update_system_config),

    url(r'^api/event/eventBook$', views.book_event),

    url(r'^api/event/eventMyBook$', views.get_booked_events),

    url(r'^api/event/eventMyPublish$', views.get_published_events),

    url(r'^api/users/userInfoGet$', views.get_user_info),

    url(r'^api/users/userInfoSet$', views.set_user_info),

    url(r'^api/users/userSpace$', views.get_user_space),

    url(r'^api/login/register$', views.user_register),

    url(r'^api/login/login$', views.user_login),

    url(r'^api/public/feedback$', views.post_feedback),

    url(r'^api/public/upLoadImg$', views.upload_image),

    url(r'^api/chat/getNoRead$', views.get_noreads),

    url(r'^api/chat/friendAdd$', views.follow_or_unfollow_user),

    url(r'^api/chat/friendList$', views.get_following_users),

    url(r'^api/login/sendVerify$', views.send_verify),

    url(r'^api/login/changePwd$', views.change_pwd),

    url(r'^api/chat/sendMsg$', views.send_message),

    url(r'^api/chat/chatList$', views.get_chat_list),

    url(r'^api/chat/chatFriend$', views.get_chat_friend),

    url(r'^get-uid-by-sessionkey$', views.get_uid_by_sessionkey),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

