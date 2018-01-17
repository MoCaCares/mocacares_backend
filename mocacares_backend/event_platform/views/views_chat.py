from .views_event import *
from .views_user import *
from ..models import *
from ..util import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user, login, authenticate
from django.db import IntegrityError


def get_noreads(request):
    return JsonResponse(api_returned_object(info={
        'new_msg': '0',
        'new_comment': '0'
    }))







