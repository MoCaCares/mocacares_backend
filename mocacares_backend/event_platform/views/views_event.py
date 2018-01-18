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










