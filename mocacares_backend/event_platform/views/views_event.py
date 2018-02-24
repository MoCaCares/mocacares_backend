import json

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
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='You need to log in to view your comments.')

    my_comments = Comment.objects.filter(poster=user)
    return JsonResponse(api_returned_object(info=list(my_comments)), encoder=CommentEncoder)


def update_system_config(request):
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='You need to log in to update your preferences.')


    try:
        recommend = json.loads(request.POST.get('recommend', None))
        if set(recommend) - {'1', '2', '3', '4'}:
            return response_of_failure(msg='Invalid setting value')
        notify = json.loads(request.POST.get('notify', None))
        if set(notify) - {'1', '2'}:
            return response_of_failure(msg='Invalid setting value')
        receive = json.loads(request.POST.get('receive', None))
        if set(receive) - {'1'}:
            return response_of_failure(msg='Invalid setting value')
    except json.decoder.JSONDecodeError:
        return response_of_failure(msg='Invalid setting value')

    system_config = user.system_config

    if recommend:
        system_config.recommend = json.dumps(recommend)
    if notify:
        system_config.notify = json.dumps(notify)
    if receive:
        system_config.receive = json.dumps(receive)
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


def _unify_date_format(date_str):
    format_1_to_be_changed = '%Y-%m-%d'
    format_2_to_be_changed = '(null),%d %b'
    correct_format = '%A,%d %b'
    try:
        return datetime.strptime(date_str, format_1_to_be_changed).strftime(correct_format)
    except ValueError:
        try:
            return datetime.strptime(date_str, format_2_to_be_changed).strftime(correct_format)
        except ValueError:
            return date_str

def _unify_time_format(time_str):
    format_to_be_changed = '%H:%M:%S'
    correct_format = '%I:%M %p'
    try:
        return datetime.strptime(time_str, format_to_be_changed).strftime(correct_format)
    except ValueError:
        return time_str

def _change_time_str_format(time_str):
    hour_min = time_str.split(':')
    if hour_min[0] == '0':
        hour_min[0] = '12'
    return ':'.join(hour_min)

def add_or_edit_event(request):
    print(request.POST)
    print()
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='You need to log in to post or edit an event.')

    if user.user_type != 2:
        return response_of_failure(msg='No permission')

    required_keys = ['title', 'type', 'time_type', 'desrc', 'hour_start', 'hour_end', 'begin_time']
    if not all([field in request.POST for field in required_keys]):
        return response_of_failure('Invalid event')

    all_keys = ['type', 'title', 'content', 'desrc', 'add', 'question', 'time_type', 'week']

    begin_time = _unify_date_format(request.POST['begin_time'])

    hour_start = _change_time_str_format(_unify_time_format(request.POST['hour_start']))
    hour_end = _change_time_str_format(_unify_time_format(request.POST['hour_end']))

    datetime_format = '%Y %A,%d %b %I:%M %p'
    year_str = str(datetime.now().year)
    start_time = datetime.strptime(year_str + ' ' + begin_time + ' ' + hour_start, datetime_format)
    end_time = datetime.strptime(year_str + ' ' + begin_time + ' ' + hour_end, datetime_format)

    key_mapping = {'type': 'event_type_id', 'desrc': 'description', 'add': 'address'}

    event = None
    if 'aid' in request.POST:
        try:
            event = Event.objects.get(pk=request.POST['aid'])
        except ObjectDoesNotExist:
            return response_of_failure(msg='Event not found')
    else:
        event = Event()

    for key in all_keys:
        value = request.POST.get(key, None)
        model_key = key_mapping.get(key, None) or key
        setattr(event, model_key, value)

    if 'img' in request.POST:
        try:
            image_url = request.POST['img']
            img = UploadedImage.objects.get(image_url=image_url)
            event.img = img
        except ObjectDoesNotExist:
            return response_of_failure(msg='Image does not exist')
            pass

    event.start_time = start_time
    event.end_time = end_time
    event.poster_id = user.id

    event.save()
    return JsonResponse({
        'code': 1,
        'msg': 'Success'
    })


def delete_event(request):
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='You need to log in first.')

    user_type = user.user_type
    if user_type != 2:
        return response_of_failure(msg='No permission')
    event_id = request.POST['aid']
    try:
        event = Event.objects.get(pk=event_id)
        event.delete()
        return response_of_success(msg='Success')
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
    event_types = EventType.objects.all()
    return JsonResponse(api_returned_object(info=list(event_types)), encoder=EventTypeEncoder)


def get_recommended_events(request):
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='You need to log in to view events.')

    page = int(request.POST.get('page', 1)) - 1
    page_end = page + 6
    event_type = request.POST.getlist('type[]')

    events = Event.objects.filter(event_type_id__in=event_type)[page:page_end]
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
