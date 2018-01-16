from .views_event import *
from .views_user import *
from ..models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user, login, authenticate


def user_login(request):
    input_email_address = request.POST['email']
    input_password = request.POST['password']
    user = authenticate(email_address=input_email_address, password=input_password)
    if user is not None:
        if user.is_active:
            login(request, user)
            user_session_key = request.session.session_key
            return JsonResponse({
                'code': 1,
                'info': {
                    '_token': user_session_key,
                },
                'msg': 'login success'
            }, status=200)
        else:
            return HttpResponse("account is not active", status=500)
    else:
        return HttpResponse("account not found", status=404)


def get_user_space(request):
    user = get_user(request)
    return JsonResponse({})





