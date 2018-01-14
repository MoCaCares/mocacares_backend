from django.core.serializers.json import DjangoJSONEncoder
from .models import *


class UserEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {

            }
        return super(UserEncoder, self).default(obj)


class EventEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Event):
            return {

            }
        return super(EventEncoder, self).default(obj)


class CommentEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Comment):
            return {
                
            }
        return super(CommentEncoder, self).default(obj)



