from ..models import *
from ..encoder import *
from ..util import *
from .util import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from datetime import datetime
import random


def get_comments(request):
    if 'aid' in request.POST:
        event = Event.objects.get(pk=request.POST['aid'])
        comments = list(event.comment_set.all())
        return JsonResponse(api_returned_object(info=comments), encoder=CommentEncoder)
    return response_of_failure(msg='Event ID not given')


def get_my_comments(request):
    if '_token' not in request.POST:
        return response_of_failure(msg='Invalid token')

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='You need to log in to view your comments.')

    my_comments = Comment.objects.filter(poster=user)
    return JsonResponse(api_returned_object(info=list(my_comments)), encoder=CommentEncoder)


def update_system_config(request):
    if '_token' not in request.POST:
        return response_of_failure(msg='Invalid token')

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='You need to log in to update your preferences.')

    recommend = request.POST.get('recommend', None)
    if recommend not in ['1', '2', '3', '4']:
        return response_of_failure(msg='Invalid setting value')
    notify = request.POST.get('notify', None)
    if notify not in ['1', '2']:
        return response_of_failure(msg='Invalid setting value')
    receive = request.POST.get('receive', None)
    if receive not in ['1']:
        return response_of_failure(msg='Invalid setting value')

    system_config = user.system_config

    if recommend:
        system_config.recommend = recommend
    if notify:
        system_config.notify = notify
    if receive:
        system_config.receive = receive
    system_config.save()
    return JsonResponse({
        'code': 1,
        'msg': 'Success'
    })


def get_events(request):
    page = 1
    event_type = None
    search_key = None

    if 'type' in request.POST:
        event_type_id = request.POST['type']
        event_type = EventType.objects.get(pk=event_type_id)
    if 'search' in request.POST:
        search_key = request.POST['search']

    events = Event.objects.all()
    if event_type is not None:
        events = events.filter(event_type=event_type)
    if search_key is not None:
        events = events.filter(Q(title__icontains=search_key) | Q(description__icontains=search_key))

    return JsonResponse(api_returned_object(info=list(events)), encoder=EventSummaryEncoder)


def add_event(request):
    if '_token' not in request.POST:
        return response_of_failure(msg='Invalid token')

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='You need to log in to post an event.')

    if user.user_type != 2:
        return response_of_failure(msg='No permission')

    required_keys = ['title', 'type', 'time_type', 'desrc', 'hour_start', 'hour_end', 'begin_time']
    if not all([field in request.POST for field in required_keys]):
        return response_of_failure('Invalid event')

    all_keys = ['type', 'title', 'content', 'desrc', 'add', 'question', 'time_type', 'week']

    begin_time = request.POST['begin_time']
    hour_start = request.POST['hour_start']
    hour_end = request.POST['hour_end']

    datetime_format = '%Y %A,%d %b %I:%M %p'
    year_str = str(datetime.now().year)
    start_time = datetime.strptime(year_str + ' ' + begin_time + ' ' + hour_start, datetime_format)
    end_time = datetime.strptime(year_str + ' ' + begin_time + ' ' + hour_end, datetime_format)

    key_mapping = {'type': 'event_type_id', 'desrc': 'description', 'add': 'address'}

    new_event = Event()
    for key in all_keys:
        value = request.POST.get(key, None)
        model_key = key_mapping.get(key, None) or key
        setattr(new_event, model_key, value)

    image_url = request.POST['img']
    try:
        img = UploadedImage.objects.get(image_url=image_url)
    except ObjectDoesNotExist:
        return response_of_failure(msg='Image does not exist')

    new_event.img = img
    new_event.start_time = start_time
    new_event.end_time = end_time
    new_event.poster_id = user.id

    new_event.save()
    return JsonResponse({
        'code': 1,
        'msg': 'Success'
    })


def delete_event(request):
    user = get_user(request)
    user_type = user.user_type
    if user_type != 2:
        return JsonResponse({
            'code': 0,
            'msg': 'No permission'
        })
    event_id = request.POST['aid']
    try:
        event = Event.objects.get(pk=event_id)
        event.delete()
        return JsonResponse({
            'code': 1,
            'msg': 'Success'
        })
    except ObjectDoesNotExist:
        return response_of_failure(msg='event cannot be found')


def get_event(request):
    event_id = request.POST['aid']
    try:
        event = Event.objects.get(pk=event_id)
        return JsonResponse({
            'code': 1,
            'msg': '',
            'info': event
        }, encoder=EventDetailEncoder)
    except ObjectDoesNotExist:
        return response_of_failure(msg='event cannot be found')


def get_event_types(request):
    event_types = list(EventType.objects.all())
    response = []
    for event_type in event_types:
        response.append({
            'id': event_type.pk,
            'name': event_type.name,
            'img': 'https://www.newstatesman.com/sites/all/themes/creative-responsive-theme/images/new_statesman_events.jpg'
        })
    return JsonResponse(api_returned_object(info=response))


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


def get_recommended_events(request):
    if '_token' not in request.POST:
        return response_of_failure(msg='Invalid token')

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='You need to log in to view events.')

    page = int(request.POST.get('page', 1)) - 1
    page_end = page + 6
    event_type = request.POST.get('type', None)

    print(event_type)

    events = Event.objects.filter(event_type_id__in=event_type)[page:page_end]\
             if event_type else\
             Event.objects.all()[page:page_end]

    if not events:
        return response_of_failure(msg='No matching events.')

    return JsonResponse(api_returned_object(info=list(events)), encoder=EventSummaryEncoder)



# public function eventRecommend() {
#     $uid = $this->_checkToken();
#     $mod = D('Article');
#     //分类
# //      $type = json_decode(I('post.type'), true);
#     $type = I('post.type');
#     if (!empty($type)) {
#         $where['type'] = array('IN', $type);
#     }
#     //分页
#     $page = I('post.page');
#     if (empty($page)) {
#         $page = 1; //默认分页为1
#     }
#     $where['status'] = 1;
#     $list = $mod->where($where)->page($page, 6)->order('id DESC')->field('id,time_type,hour_start,hour_end,week,begin_time,title,img,desrc,type,add')
#             ->simpJoin('ArticleType', 'type', 'id', 'name', 't_')
#             ->select();
#     if (empty($list)) {
#         $this->apiReturn(1, 'No match event');
#     } else {
#         $this->apiReturn(1, '', $list);
#     }
# }


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
