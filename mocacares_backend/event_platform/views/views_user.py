from .views_event import *
from ..models import *
from ..util import *
from .util import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from django.db import IntegrityError


import redis
REDIS_DOMAIN = '0.0.0.0'
REDIS_PORT = 6379

strict_redis = redis.StrictRedis(
    host=REDIS_DOMAIN,
    port=REDIS_PORT,
    db=0
)


def user_login(request):
    input_email_address = request.POST['email']
    input_password = request.POST['password']
    user = authenticate(email_address=input_email_address, password=input_password)
    if user is not None:
        if user.is_active:
            login(request, user)
            if request.session.session_key is None:
                request.session.save()
            print('login: ' + str(request.session.session_key))
            return JsonResponse({
                'code': 1,
                'info': {
                    '_token': request.session.session_key,
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

    if not validate_email_format(email):
        return response_of_failure('incorrect email address format')
    if not validate_password_format(password):
        return response_of_failure('password must contain at least 6 digits')
    if not validate_user_type(user_type):
        return response_of_failure('unexisting user type')

    try:
        new_system_config = SystemConfig()
        new_system_config.save()
        new_user = User(
            username=username, 
            email_address=email, 
            user_type=user_type, 
            system_config=new_system_config
        )
        new_user.set_password(password)
        new_user.save()

        new_session = SessionStore()
        new_session.create()
        request.session = new_session
        request.session.modified = True
        print('register: ' + str(request.session.session_key))

        login(request, new_user)
        return JsonResponse({
            'code': 1,
            'info': {
                '_token': request.session.session_key,
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
    

def set_user_info(request):
    def parse_boolean(i):
        if not (i == '1' or i == '0'):
            return None
        return True if i == '1' else False
    
    if '_token' not in request.POST:
        return response_of_failure('missing field(s)')
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to login first')

    print('update user profile:\n' + str(request.POST))
    if 'username' in request.POST:
        user.username = request.POST['username']
    if 'occupation' in request.POST:
        user.username = request.POST['occupation']
    if 'statement' in request.POST:
        user.username = request.POST['statement']
    if 'img' in request.POST:
        user.portrait = UploadedImage.objects.get(image_url=request.POST['img'])
    if 'age' in request.POST:
        try:
            user.username = int(request.POST['age'])
        except Exception:
            pass
    if 'gender' in request.POST:
        try:
            user.gender = int(request.POST['sex'])
        except Exception:
            pass
    user.save()

    config = user.system_config
    if 'is_show_email' in request.POST:
        if parse_boolean(request.POST['is_show_email']) is not None:
            config.is_show_email = parse_boolean(request.POST['is_show_email'])
    if 'is_show_event' in request.POST:
        if parse_boolean(request.POST['is_show_event']) is not None:
            config.is_show_events = parse_boolean(request.POST['is_show_event']) 
    config.save()

    return response_of_success(msg='update successfully')


def get_user_space(request):
    if 'uid' not in request.POST or '_token' not in request.POST:
        return response_of_failure('missing field(s)')
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to login first')

    try:
        target_user = User.objects.get(pk=request.POST['uid'])
        target_user_json = UserInfoEncoder().default(target_user)

        target_user_space_json = {}
        target_user_space_json['user'] = target_user_json
        if target_user.system_config.is_show_events:
            target_user_space_json['event'] = list(target_user.participated_event_set.all())
        else:
            target_user_space_json['event'] = []
        
        if target_user in user.follower_set.all():
            target_user_space_json['is_friend'] = '1'
        else:
            target_user_space_json['is_friend'] = '0'
    except ObjectDoesNotExist:
        return response_of_failure(msg='target user not found')

    print(api_returned_object(info=target_user_space_json))
    return JsonResponse(api_returned_object(info=target_user_space_json), encoder=EventSummaryEncoder)


def change_pwd(request):
    if '_token' not in request.POST:
        return response_of_failure(msg='Invalid token')

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='You need to log in to change password.')

    if 'verify' not in request.POST:
        return response_of_failure(msg='Verification code not provided.')

    if 'newpwd' not in request.POST:
        return response_of_failure(msg='New password not provided.')

    verification_code = request.POST['verify']
    new_pwd = request.POST['newpwd']
    token = request.POST['_token']

    if not token_vericode_pair_exists(token=token, verification_code=verification_code):
        return response_of_failure(msg='Invalid token or verification code.')

    if not validate_password_format(new_pwd):
        return response_of_failure(msg='password must contain at least 6 digits')
    user.set_password(new_pwd)
    user.save()

    return JsonResponse({
        'code': 1,
        'msg': 'Password changed successfully.'
    }, status=200)


def send_verify(request):
    if '_token' not in request.POST:
        return response_of_failure(msg='Invalid token')

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='You need to log in to change password.')

    token = request.POST['_token']

    verification_code = random.randint(0, 99999)
    verification_code_str = str(verification_code).zfill(5)

    save_token_vericode_pair(token=token, verification_code=verification_code_str)

    EmailThread(
        subject = 'MocaCare Verification Code',
        content = 'Your verification code is {}'.format(verification_code_str),
        receiver_list = [user.email_address]
    ).start()

    #TODO: Image OneToOne

    return JsonResponse({
        'code': 1,
        'msg': 'Verification code sent successfully.'
    }, status=200)


# Temp

def save_token_vericode_pair(token, verification_code):
    query = TokenVerificationPair.objects.filter(token=token)
    if query:
        pair = query[0]
        pair.verification_code = verification_code
        pair.save()
    else:
        pair = TokenVerificationPair(token=token, verification_code=verification_code)
        pair.save()


def token_vericode_pair_exists(token, verification_code=None):
    query = TokenVerificationPair.objects.filter(token=token, verification_code=verification_code)
    if query:
        query[0].delete()
        return True
    return False

