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
        if set(notify) - {'1', '2', '3'}:
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
        keyword_matching_events = events.filter(Q(title__icontains=search_key) | Q(description__icontains=search_key))
        keyword_matching_users = User.objects.filter(Q(username__icontains=search_key) | Q(statement__icontains=search_key))
        events_posted_by_matching_users = events.filter(poster__in=keyword_matching_users)
        events = keyword_matching_events.union(events_posted_by_matching_users)

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
            if event.poster.pk != user.pk:
                return response_of_failure(msg='No permission: you are not the owner of the event')
        except ObjectDoesNotExist:
            return response_of_failure(msg='Edited event not found')
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
    event.poster = user

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
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='You need to log in first.')

    event_id = request.POST['aid']
    try:
        event = Event.objects.get(pk=event_id)
        json_response = EventDetailEncoder().default(event)
        json_response['isbook'] = '1'  if user in event.followers.all() else '0'
        json_response['ispart'] = '1'  if user in event.participants.all() else '0'
        return JsonResponse(api_returned_object(info=json_response))
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
    if page < 0:
        return response_of_failure(msg='Invalid page value.')
    page_end = page + 6
    event_type = request.POST.getlist('type[]')

    recommend_settings = json.loads(user.system_config.recommend)
    recommended_events = Event.objects.none()

    following_users = user.following_users.all()

    if 1 in recommend_settings:
        # Recommend events bookmarked by users I follow
        bookmarked_events = [u.bookmarked_event_set.all() for u in following_users]
        recommended_events = recommended_events.union(*bookmarked_events)
    if 2 in recommend_settings:
        # Recommend events participated by users I follow
        participated_events = [u.participated_event_set.all() for u in following_users]
        recommended_events = recommended_events.union(*participated_events)
    if 3 in recommend_settings:
        # Recommend events of the same categories as my past events
        event_types = [event.event_type for event in user.participated_event_set.all()]
        category_matching_events = Event.objects.filter(event_type__in = event_types)
        recommended_events = recommended_events.union(category_matching_events)
    if 4 in recommend_settings:
        # Recommend events of the same organizer as my past events
        posters = [event.poster for event in user.participated_event_set.all()]
        poster_matching_events = Event.objects.filter(poster__in = posters)
        recommended_events = recommended_events.union(poster_matching_events)

    recommended_events = list(recommended_events)

    if event_type:
        recommended_events = [x for x in recommended_events if str(x.event_type_id) in event_type]

    recommended_events = recommended_events[page:page_end]
    return JsonResponse(api_returned_object(info=list(recommended_events)), encoder=EventSummaryEncoder)



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
