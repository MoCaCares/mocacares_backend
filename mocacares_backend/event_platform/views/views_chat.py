import redis
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse

from ..models import *
from ..util import *
from .views_event import *
from .views_user import *

REDIS_DOMAIN = '0.0.0.0'
REDIS_PORT = 6379


def get_noreads(request):
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to login first')

    return JsonResponse(api_returned_object(info={
        'new_msg': Message.objects.filter(read=False, receiver=user).count(),
        'new_comment': '0',  # TODO: calculate and return
    }))


def follow_or_unfollow_user(request):
    if 'fid' not in request.POST:
        return response_of_failure(msg='missing field(s)')

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to login first')

    try:
        target_user = User.objects.get(pk=request.POST['fid'])
        if target_user in user.following_users.all():
            user.following_users.remove(target_user)
            status = '0'
        else:
            user.following_users.add(target_user)
            status = '1'
    except ObjectDoesNotExist:
        return response_of_failure(msg='target user not found')

    return JsonResponse({
        'code': 1,
        'msg': 'Success',
        'info': status
    })


def get_following_users(request):
    if 'type' not in request.POST:
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
    if 'sid' not in request.POST or 'msg' not in request.POST:
        return response_of_failure(msg='missing field(s)')
    if request.POST['msg'] == '':
        return response_of_success(msg='empty message is not sent')
    
    sender = get_user(request)
    if isinstance(sender, AnonymousUser):
        return response_of_failure(msg='you need to login to send message')
    
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
    if 'sid' not in request.POST:
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
                "img": get_image_url(other.portrait),
                'statement': 'statement',
                'no_read': messages.filter(read=False, receiver=user).count(),
            })
    return JsonResponse(api_returned_object(info=chat_friends))
