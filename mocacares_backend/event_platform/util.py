from importlib import import_module
from random import randint

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse, JsonResponse
from django.utils.encoding import uri_to_iri
from django.utils.module_loading import import_string

from .models import *

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


def load_backend(path):
    return import_string(path)()


def get_user(request):
    session = None
    if '_token' in request.POST:
        session = SessionStore(session_key=request.POST['_token'])
    elif '_token' in request.GET:
        session = SessionStore(session_key=request.GET['_token'])
    if session is None or '_auth_user_id' not in session or '_auth_user_backend' not in session:
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


def get_image_url(uploaded_image):
    default = ''
    if not uploaded_image or not uploaded_image.image_url:
        return default
    return uploaded_image.image_url
