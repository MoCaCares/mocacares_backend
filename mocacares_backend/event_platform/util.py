from .models import *
from django.contrib.auth.models import AnonymousUser
from importlib import import_module
from django.conf import settings
from django.utils.module_loading import import_string


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
    backend_path = session['_auth_user_backen']
    
    if backend_path in settings.AUTHENTICATION_BACKENDS:
        backend = load_backend(backend_path)
        user = backend.get_user(user_id)
        # TODO: Verify the session
        
    return user or AnonymousUser()