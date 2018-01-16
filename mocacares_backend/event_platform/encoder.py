from django.core.serializers.json import DjangoJSONEncoder
from .models import *


class UserEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {

            }
        return super(UserEncoder, self).default(obj)


class EventSummaryEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Event):
            return {
                "id": obj.pk,
                "start_time": "0000-00-00 00:00:00",
                "end_time": "0000-00-00 00:00:00",
                "content": "hellodhjsds",
                "title": obj.title,
                "img": "http://mainstreamevents.homestead.com/Event_Picture.jpg",
                "desrc": obj.description,
                "add": obj.address,
                "type": obj.event_type.pk, 
                "t_name": obj.event_type.name
            }
        return super(EventEncoder, self).default(obj)


class EventDetailEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Event):
            return {
                "id": obj.pk,
                "start_time": "0000-00-00 00:00:00",
                "end_time": "0000-00-00 00:00:00",
                "title": obj.title,
                "img": "http://mainstreamevents.homestead.com/Event_Picture.jpg",
                "desrc": obj.description,
                "add": obj.address,
                "type": obj.event_type.pk, 
                "t_name": obj.event_type.name,
                "uid": obj.poster.pk,
                "u_img": "http://apoimg-10058029.image.myqcloud.com/test_fileId_387da613-7632-4c6b-864d-052fa1358683",

            }
        return super(EventEncoder, self).default(obj)


class CommentEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Comment):
            return {
                "id": obj.pk,
                "uid": obj.poster.pk,
                "aid": obj.target_event.pk,
                "content": obj.content,
                "c_time": obj.post_time,  # "0000-00-00 00:00:00"
                "u_username": obj.poster.username,
                "u_mg": "http://apoimg-10058029.image.myqcloud.com/test_fileId_387da613-7632-4c6b-864d-052fa1358683"
            }
        return super(CommentEncoder, self).default(obj)



