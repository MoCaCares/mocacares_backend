from ..models import *
from ..encoder import *
from ..util import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.db.models import Q


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

    system_config = SystemConfig.objects.filter(target_user=user).first()
    if not system_config:
        system_config = SystemConfig(target_user=user, recommend=recommend, notify=notify, receive=receive)
        system_config.save()
        return JsonResponse({
            'code': 1,
            'msg': 'Success'
        })

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
    pass


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
