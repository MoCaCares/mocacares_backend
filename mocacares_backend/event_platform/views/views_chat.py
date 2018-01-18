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


def follow_user(request):
    if 'fid' not in request.POST or '_token' not in request.POST:
        return response_of_failure('missing field(s)')

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to login first')

    try:
        target_user = User.objects.get(pk=request.POST['fid'])
        user.following_users.add(target_user)
    except ObjectDoesNotExist:
        return response_of_failure(msg='target user not found')

    return response_of_success(msg='success')


