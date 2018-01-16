from .views_event import *
from .views_user import *
from ..models import *
from ..encoder import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse


def get_user(request):
    return HttpResponse(status=200)


def post_comment(request):
    return HttpResponse(status=200)


def post_feedback(request):
    feedback_content = request.POST['content']
    print(feedback_content)
    return JsonResponse({
        'code': 1,
        'msg': 'feedback sent successfully'
    }, status=200)


def get_recommended_events(request):
    return HttpResponse(status=200)





