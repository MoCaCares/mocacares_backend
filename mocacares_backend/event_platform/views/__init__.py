from .views_event import *
from .views_user import *
from ..models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse


def get_user(request):
    return HttpResponse(status=200)


def get_comment_list(request):
    return HttpResponse(status=200)


def get_events_by_type(request):
    event_type = request.GET['type']
    return HttpResponse(status=200)


def get_event(request):
    event_id = request.GET['aid']
    try:
        event = Event.objects.get(pk=event_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)


def post_comment(request):
    return HttpResponse(status=200)


def get_events(request):
    return HttpResponse(status=200)


def get_event_types(request):
    return HttpResponse(status=200)


def post_feedback(request):
    feedback_content = request.POST['content']
    print(feedback_content)
    return JsonResponse({
        'msg': 'feedback sent successfully'
    }, status=200)


def get_recommended_events(request):
    return HttpResponse(status=200)





