from .views_event import *
from .views_user import *
from ..models import *
from ..util import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user, login, authenticate
from django.db import IntegrityError


def _validate_user_type(user_type):
    return user_type == '1' or user_type == '2'


def _validate_email_format(email):
    return True


def _validate_password_format(password):
    return len(password) >= 6


def user_login(request):
    input_email_address = request.POST['email']
    input_password = request.POST['password']
    user = authenticate(email_address=input_email_address, password=input_password)
    if user is not None:
        if user.is_active:
            login(request, user)
            user_session_key = request.session.session_key
            return JsonResponse({
                'code': 1,
                'info': {
                    '_token': user_session_key,
                },
                'msg': 'login success'
            })
        else:
            return response_of_failure('account is not active')
    else:
        return response_of_failure('account not found')


def user_register(request):
    form = request.POST
    if 'email' not in form or 'type' not in form or 'username' not in form or 'password' not in form:
        return response_of_failure('missing field(s)')
    username = form['username']
    email = form['email']
    password = form['password']
    user_type = form['type']

    if not _validate_email_format(email):
        return response_of_failure('incorrect email address format')
    if not _validate_password_format(password):
        return response_of_failure('password must contain at least 6 digits')
    if not _validate_user_type(user_type):
        return response_of_failure('unexisting user type')

    try:
        new_user = User(username=username, email_address=email, password=password, user_type=user_type)
        new_user.save()
        login(request, new_user)
        user_session_key = request.session.session_key
        return JsonResponse({
            'code': 1,
            'info': {
                '_token': user_session_key,
            },
            'msg': 'login success'
        })
    except IntegrityError:
        return response_of_failure('username or email already exists')


def get_user_info(request):
    if '_token' not in request.POST:
        return response_of_failure('missing field(s)')
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to login first')
    return JsonResponse(api_returned_object(info=user), encoder=UserInfoEncoder)


def get_user_space(request):
    if 'uid' not in request.POST or '_token' not in request.POST:
        return response_of_failure('missing field(s)')
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to login first')

    try:
        target_user = User.objects.get(pk=request.POST['uid'])
        target_user_json = UserInfoEncoder().default(target_user)
        target_user_json['statement'] = 'to be add'
        target_user_json['occupation'] = 'to be add'
        
        target_user_space_json = {}
        target_user_space_json['user'] = target_user_json
        target_user_space_json['event'] = []

        if target_user in user.follower_set.all():
            target_user_space_json['is_friend'] = '1'
        else:
            target_user_space_json['is_friend'] = '0'
    except ObjectDoesNotExist:
        return response_of_failure(msg='target user not found')

    print(target_user_space_json)
    return JsonResponse(api_returned_object(info=target_user_space_json))





