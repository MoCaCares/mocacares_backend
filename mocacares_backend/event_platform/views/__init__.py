from .views_event import *
from .views_user import *
from ..models import *
from ..encoder import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import AnonymousUser
from ..util import get_user


def get_user_info(request):
    return HttpResponse(status=200)


def post_comment(request):
    if '_token' not in request.POST or 'aid' not in request.POST or 'content' not in request.POST:
        return JsonResponse({
            'code': 0,
            'msg': 'invalid request'
        }, status=400)

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return JsonResponse({
            'code': 0,
            'msg': 'You need to log in to post comment'
        }, status=400) 
    
    event = Event.objects.get(pk=request.POST['aid'])
    comment = Comment(poster=user, target_event=event, content=request.POST['content'])
    comment.save()
    return JsonResponse({
        'code': 1,
        'msg': 'success'
    })


def post_feedback(request):
    feedback_content = request.POST['content']
    return JsonResponse({
        'code': 1,
        'msg': 'feedback sent successfully'
    }, status=200)


def get_recommended_events(request):
    return HttpResponse(status=200)


def book_event(request):
    if 'aid' not in request.POST or '_token' not in request.POST or 'type' not in request.POST:
        return JsonResponse({
            'code': 0,
            'msg': 'invalid request'
        }, status=400)
    user = get_user(request)
    event = Event.objects.get(pk=request.POST['aid'])
    if request.POST['type'] == '1':
        event.participants.add(user)
    elif request.POST['type'] == '2':
        event.followers.add(user)
    else:
        return JsonResponse({
            'code': 0,
            'msg': 'invalid request'
        }, status=400)
    return JsonResponse({
        'code': 1,
        'msg': 'success'
    })


def get_booked_events(request):
    if '_token' not in request.POST or 'type' not in request.POST:
        return JsonResponse({
            'code': 0,
            'msg': 'invalid request'
        }, status=400)
    user = get_user(request)
    if request.POST['type'] == '1':
        events = user.participated_event_set.all()
    elif request.POST['type'] == '2':
        events = user.bookmarked_event_set.all()
    else:
        return JsonResponse({
            'code': 0,
            'msg': 'invalid request'
        }, status=400)
    return JsonResponse({
        'code': 1,
        'msg': 'success',
        'info': list(events)
    }, encoder=EventSummaryEncoder)










