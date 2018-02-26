from django.contrib.auth.models import AnonymousUser
from django.core.serializers.json import DjangoJSONEncoder

from .models import *
from .util import get_image_url


def format_datetime(datetime):
    return datetime.strftime("%Y-%m-%d %H:%M:%S")

def datetime_to_date_str(datetime):
    return datetime.strftime("%Y-%m-%d")

def datetime_to_time_str(datetime):
    return datetime.strftime("%H:%M:%S")

def parse_bool_to_int(b):
    return "1" if b else "0"


class UserInfoEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                "id": obj.pk,
                "username": obj.username,
                "type": obj.user_type,
                "img": get_image_url(obj.portrait),
                "email": obj.email_address,
                "statement": obj.statement,
                "occupation": obj.occupation,
                "age": obj.age,
                "sex": obj.gender,
                "is_show_event": parse_bool_to_int(obj.system_config.is_show_events),
                "is_show_email": parse_bool_to_int(obj.system_config.is_show_email),
            }
        return super(UserInfoEncoder, self).default(obj)


class EventTypeEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, EventType):
            return {
                "id": obj.pk,
                "name": obj.name,
                "img": get_image_url(obj.img)
            }
        return super(EventTypeEncoder, self).default(obj)


class EventSummaryEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Event):
            return {
                "id": obj.pk,
                "aid": obj.pk,
                "uid": obj.poster.pk,
                "week": "1",
                "begin_time": datetime_to_date_str(obj.start_time),
                "hour_start": datetime_to_time_str(obj.start_time),
                "hour_end": datetime_to_time_str(obj.end_time),
                "time_type": "1",
                "content": "hellodhjsds",
                "title": obj.title,
                "img": get_image_url(obj.img),
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
                "uid": obj.poster.pk,
                "u_img": get_image_url(obj.poster.portrait),
                "week": "1",
                "begin_time": datetime_to_date_str(obj.start_time),
                "hour_start": datetime_to_time_str(obj.start_time),
                "hour_end": datetime_to_time_str(obj.end_time),
                "time_type": "1",
                "title": obj.title,
                "img": get_image_url(obj.img),
                "desrc": obj.description,
                "add": obj.address,
                "type": obj.event_type.pk,
                "t_name": obj.event_type.name,
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
                "u_img": get_image_url(obj.poster.portrait),
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
                "u_img": get_image_url(obj.portrait),
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
                "f_img": get_image_url(obj.sender.portrait),
                "s_username": obj.receiver.username,
                "s_img": get_image_url(obj.receiver.portrait),
            }
        return super(MessageEncoder, self).default(obj)
