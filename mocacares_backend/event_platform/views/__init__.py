from .views_event import *
from .views_user import *
from ..models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse


def get_user(request):
    pass


def get_comment_list(request):
    pass


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
    pass