from .views_event import *
from .views_user import *
from .views_chat import *
from .util import *
from ..models import *
from ..encoder import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import AnonymousUser
from ..util import get_user
import imghdr
from django.core.exceptions import ValidationError


IMAGE_TYPE = ['jpeg', 'png']


def post_comment(request):
    if 'aid' not in request.POST or 'content' not in request.POST:
        return response_of_failure(msg='missing field(s)')

    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to log in to post comment')

    event = Event.objects.get(pk=request.POST['aid'])
    comment = Comment(poster=user, target_event=event, content=request.POST['content'])
    comment.save()
    return response_of_success(msg='success')


def post_feedback(request):
    feedback_content = request.POST['content']
    if feedback_content == '':
        return response_of_failure(msg='Feedback content cannot be empty')
    else:
        EmailThread(
            subject='feedback from user',
            content=feedback_content,
            receiver_list=['royl8@qq.com']
        ).start()
        return response_of_success(msg='Thanks for your valuable feedback')


def book_event(request):
    if 'aid' not in request.POST or 'type' not in request.POST:
        return response_of_failure(msg='missing fields(s)')
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='You need to log in first to book event')

    event = Event.objects.get(pk=request.POST['aid'])
    if request.POST['type'] == '1':
        if user in event.participants.all():
            event.participants.remove(user)
            status = '0'
        else:
            event.participants.add(user)
            status = '1'
    elif request.POST['type'] == '2':
        if user in event.followers.all():
            event.followers.remove(user)
            status = '0'
        else:
            event.followers.add(user)
            status = '1'
    else:
        return JsonResponse({
            'code': 0,
            'msg': 'invalid request'
        }, status=400)
    return JsonResponse({
        'code': 1,
        'msg': 'Success',
        'info': status
    })


def get_booked_events(request):
    if 'type' not in request.POST:
        return response_of_failure(msg="missing field(s)")
    user = get_user(request)
    if isinstance(user, AnonymousUser):
        return response_of_failure(msg='you need to log in first')

    if request.POST['type'] == '1':
        events = user.participated_event_set.all()
    elif request.POST['type'] == '2':
        events = user.bookmarked_event_set.all()
    else:
        return response_of_failure("invalid request")
    return JsonResponse({
        'code': 1,
        'msg': 'success',
        'info': list(events)
    }, encoder=EventCalendarEncoder)


def get_published_events(request):
    if 'page' not in request.POST:
        return JsonResponse({
            'code': 0,
            'msg': 'invalid request'
        }, status=400)
    user = get_user(request)
    events = Event.objects.filter(poster=user)
    return JsonResponse({
        'code': 1,
        'msg': 'success',
        'info': list(events)
    }, encoder=EventSummaryEncoder)


def upload_image(request):
    if 'filename' not in request.FILES:
        return response_of_failure(msg='missing field(s)')

    file_type = imghdr.what(request.FILES['filename'])
    if file_type not in IMAGE_TYPE:
        return response_of_failure(msg='Uploaded file is of invalid type')

    uploaded_image = UploadedImage(image=request.FILES['filename'])
    try:
        uploaded_image.save()
    except ValidationError as err:
        return response_of_failure(msg=err.message)
    return JsonResponse(api_returned_object(info=uploaded_image.image_url))


def get_image(request, pk):
    image = UploadedImage.objects.get(pk=pk).image
    content = image.storage.open(mode='r', name=image.name).read()
    return HttpResponse(content, content_type='image')


def get_uid_by_sessionkey(request):
    user = get_user(request)
    return HttpResponse(str(user.pk))



