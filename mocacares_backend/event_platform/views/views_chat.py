from .views_event import *
from .views_user import *
from ..models import *
from ..util import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user, login, authenticate
from django.db import IntegrityError

import redis
REDIS_DOMAIN = '0.0.0.0'
REDIS_PORT = 6379

def get_noreads(request):
    return JsonResponse(api_returned_object(info={
        'new_msg': '0',
        'new_comment': '0'
    }))


def follow_or_unfollow_user(request):
    if 'fid' not in request.POST or '_token' not in request.POST:
        return response_of_failure(msg='missing field(s)')

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to login first')

    try:
        target_user = User.objects.get(pk=request.POST['fid'])
        if target_user in user.following_users.all():
            user.following_users.remove(target_user)
        else:
            user.following_users.add(target_user)
    except ObjectDoesNotExist:
        return response_of_failure(msg='target user not found')

    return response_of_success(msg='success')


def get_following_users(request):
    if '_token' not in request.POST or 'type' not in request.POST:
        return response_of_failure(msg='missing field(s)')
    
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to login first')
    
    following_users = user.following_users.all()
    if request.POST['type'] == '1':
        following_users = following_users.filter(user_type=1)
    elif request.POST['type'] == '2':
        following_users = following_users.filter(user_type=2)
    else:
        return response_of_failure(msg='invalid user type')

    return JsonResponse(api_returned_object(info=list(following_users)), encoder=FriendEncoder)


def send_message(request):
    print(request.POST)
    sender = get_user(request)
    receiver = User.objects.get(pk=request.POST['sid'])
    message = Message(sender=sender, receiver=receiver, content=request.POST['msg'])
    message.save()
    strict_redis = redis.StrictRedis(
        host=REDIS_DOMAIN,
        port=REDIS_PORT,
        db=0
    )
    strict_redis.publish('new_messages', MessageEncoder().default(message))
    return response_of_success(msg='success')


def get_chat_list(request):
    print(request.POST)
    user = get_user(request)
    other = User.objects.get(pk=request.POST['sid'])
    messages = Message.objects.filter(Q(sender=user, receiver=other) | Q(sender=other, receiver=user)).order_by('-post_time')
    return JsonResponse(api_returned_object(info=list(messages)), encoder=MessageEncoder)






















# chat_list = [{
#         "id": "112",
#         "fid": "1",
#         "sid": "5",
#         "msg": "hello",
#         "c_time": "2017-10-18 11:13:45",
#         "status": "1",
#         "f_username": "zdg19932",
#         "f_img":   "http://apoimg-10058029.image.myqcloud.com/test_fileId_387da613-7632-4c6b-864d-052fa1358683",
#         "s_username": "123",
#         "s_img": "http://apoimg-10058029.image.myqcloud.com/test_fileId_387da613-7632-4c6b-864d-052fa1358683"
#     }, {
#         "id": "113",
#         "fid": "1",
#         "sid": "5",
#         "msg": "hello\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nhello",
#         "c_time": "2017-10-18 11:13:46",
#         "status": "1",
#         "f_username": "zdg19932",
#         "f_img":   "http://apoimg-10058029.image.myqcloud.com/test_fileId_387da613-7632-4c6b-864d-052fa1358683",
#         "s_username": "123",
#         "s_img": "http://apoimg-10058029.image.myqcloud.com/test_fileId_387da613-7632-4c6b-864d-052fa1358683"
#     }, {
#         "id": "114",
#         "fid": "1",
#         "sid": "5",
#         "msg": "hello\n\n\n\n\n\n\n\n\n\n\n\n\nhello",
#         "c_time": "2017-10-18 11:13:47",
#         "status": "1",
#         "f_username": "zdg19932",
#         "f_img":   "http://apoimg-10058029.image.myqcloud.com/test_fileId_387da613-7632-4c6b-864d-052fa1358683",
#         "s_username": "123",
#         "s_img": "http://apoimg-10058029.image.myqcloud.com/test_fileId_387da613-7632-4c6b-864d-052fa1358683"
#     }]