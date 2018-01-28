from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import AnonymousUser
from .models import *


def format_datetime(datetime):
    return datetime.strftime("%Y-%m-%d %H:%M:%S")


class UserInfoEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                "id": obj.pk,
                "username": obj.username,
                "type": obj.user_type,
                "img": "http://apoimg-10058029.image.myqcloud.com/test_fileId_387da613-7632-4c6b-864d-052fa1358683",
                "is_show_email": True,  # TODO: set accordingly
                "email": obj.email_address,
                "statement": "to be add",
                "occupation": "to be add",
                "age": "1",
                "sex": "1",
                "is_show_event": False
            }
        return super(UserInfoEncoder, self).default(obj)


class EventSummaryEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Event):
            return {
                "id": obj.pk,
                "aid": obj.pk,
                # "start_time": format_datetime(obj.start_time),
                # "end_time": format_datetime(obj.end_time),
                "week": "1",
                "begin_time": "2018-1-12",
                "hour_start": "10:12:12",
                "hour_end": "10:14:12",
                "time_type": "1",
                "content": "hellodhjsds",
                "title": obj.title,
                "img": "http://mainstreamevents.homestead.com/Event_Picture.jpg",
                "desrc": obj.description,
                "add": obj.address,
                "type": obj.event_type.pk, 
                "t_name": obj.event_type.name
            }
        return super(EventSummaryEncoder, self).default(obj)


class EventDetailEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Event):
            return {
                "id": obj.pk,
                "aid": obj.pk,
                # "start_time": format_datetime(obj.start_time),
                # "end_time": format_datetime(obj.end_time),
                "week": "1",
                "begin_time": "2018-1-12",
                "hour_start": "10:12:12",
                "hour_end": "10:14:12",
                "time_type": "1",
                "title": obj.title,
                "img": "http://mainstreamevents.homestead.com/Event_Picture.jpg",
                "desrc": obj.description,
                "add": obj.address,
                "type": obj.event_type.pk, 
                "t_name": obj.event_type.name,
                "uid": obj.poster.pk,
                "u_img": "https://www.polyvore.com/cgi/img-thing?.out=jpg&size=l&tid=85495748"
            }
        return super(EventDetailEncoder, self).default(obj)


class CommentEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Comment):
            return {
                "id": obj.pk,
                "uid": obj.poster.pk,
                "aid": obj.target_event.pk,
                "content": obj.content,
                "c_time": format_datetime(obj.post_time),  # "0000-00-00 00:00:00"
                "u_username": obj.poster.username,
                "u_img": "https://www.polyvore.com/cgi/img-thing?.out=jpg&size=l&tid=85495748"
            }
        return super(CommentEncoder, self).default(obj)


class FriendEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                "id": obj.pk,
                "uid": obj.pk,
                "fid": obj.pk,
                "u_username": obj.username,
                "u_img": "https://www.polyvore.com/cgi/img-thing?.out=jpg&size=l&tid=85495748"
            }
        return super(FriendEncoder, self).default(obj)


class MessageEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return {
                "id": obj.pk,
                "fid": obj.sender.pk,
                "sid": obj.receiver.pk,
                "msg": obj.content,
                "c_time": format_datetime(obj.post_time),
                "status": "1",
                "f_username": obj.sender.username,
                "f_img":   "http://apoimg-10058029.image.myqcloud.com/test_fileId_387da613-7632-4c6b-864d-052fa1358683",
                "s_username": obj.receiver.username,
                "s_img": "http://apoimg-10058029.image.myqcloud.com/test_fileId_387da613-7632-4c6b-864d-052fa1358683"
            }
        return super(MessageEncoder, self).default(obj)









