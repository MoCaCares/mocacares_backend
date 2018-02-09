from .views_event import *
from .views_user import *
from ..models import *
from ..util import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError

import redis
REDIS_DOMAIN = '0.0.0.0'
REDIS_PORT = 6379


def get_noreads(request):
    if '_token' not in request.POST:
        return response_of_failure(msg='missing field(s)')

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to login first')

    return JsonResponse(api_returned_object(info={
        'new_msg': Message.objects.filter(read=False, receiver=user).count(),
        'new_comment': '0',  # TODO: calculate and return
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
    if '_token' not in request.POST or 'sid' not in request.POST or 'msg' not in request.POST:
        return response_of_failure(msg='missing field(s)')
    if request.POST['msg'] == '':
        return response_of_success(msg='empty message is not sent')
    sender = get_user(request)
    if isinstance(sender, AnonymousUser):
        return response_of_failure(msg='you need to login first')
    
    receiver = User.objects.get(pk=request.POST['sid'])
    message = Message(sender=sender, receiver=receiver, content=request.POST['msg'], read=False)
    message.save()
    strict_redis = redis.StrictRedis(
        host=REDIS_DOMAIN,
        port=REDIS_PORT,
        db=0
    )
    strict_redis.publish('new_message', MessageEncoder().default(message))
    return response_of_success(msg='success')


# get message history between the user and another
def get_chat_list(request):
    if '_token' not in request.POST or 'sid' not in request.POST:
        return response_of_failure(msg='missing field(s)') 

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to login first')
    
    other = User.objects.get(pk=request.POST['sid'])
    messages = Message.objects.filter(Q(sender=user, receiver=other) | Q(sender=other, receiver=user)).order_by('-post_time')
    for message in messages:
        if message.receiver.pk == user.pk and message.read == False:
            message.read = True
            message.save()
    return JsonResponse(api_returned_object(info=list(messages)), encoder=MessageEncoder)


def get_chat_friend(request):
    if '_token' not in request.POST:
        return response_of_failure(msg='missing field(s)')
    
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to login first')
    
    chat_friends = []
    for other in User.objects.all():
        messages = Message.objects.filter(Q(sender=user, receiver=other) | Q(sender=other, receiver=user))
        if messages.exists():
            chat_friends.append({
                'uid': other.pk,
                'name': other.username,
                "img": "http://apoimg-10058029.image.myqcloud.com/test_fileId_387da613-7632-4c6b-864d-052fa1358683",  # TODO: return the actual image url
                'statement': 'statement',
                'no_read': messages.filter(read=False, receiver=user).count(),
            })
    return JsonResponse(api_returned_object(info=chat_friends))










