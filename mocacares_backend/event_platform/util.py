from .models import *
from django.contrib.auth.models import AnonymousUser
from importlib import import_module
from django.conf import settings
from django.utils.module_loading import import_string
from django.http import HttpResponse, JsonResponse
from random import randint


SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


def load_backend(path):
    return import_string(path)()


def get_user(request):
    session = None
    if '_token' in request.POST:
        session = SessionStore(session_key=request.POST['_token'])
    elif '_token' in request.GET:
        session = SessionStore(session_key=request.GET['_token'])
    if session is None:
        return AnonymousUser()

    user_id = session['_auth_user_id']
    backend_path = session['_auth_user_backend']

    if backend_path in settings.AUTHENTICATION_BACKENDS:
        backend = load_backend(backend_path)
        user = backend.get_user(user_id)
        # TODO: Verify the session

    return user or AnonymousUser()


def response_of_failure(msg=''):
    return JsonResponse({
        'code': '0',
        'msg': msg,
        'info': ''
    })


def response_of_success(msg=''):
    return JsonResponse({
        'code': '1',
        'msg': msg,
        'info': ''
    })


def api_returned_object(code='1', msg='', info=''):
    return {
        'code': code,
        'msg': msg,
        'info': info
    }

