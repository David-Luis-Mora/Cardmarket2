import re

from django.http import JsonResponse
import json
from .models import Token
from functools import wraps



def require_get(view_func):
    def wrapper(request, *args, **kwargs):
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return view_func(request, *args, **kwargs)

    return wrapper


def require_post(view_func):
    def wrapper(request, *args, **kwargs):
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return view_func(request, *args, **kwargs)

    return wrapper

def method_required(method):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method != method:
                return JsonResponse({'error': 'Method not allowed'}, status=405)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



def validate_json(required_fields=None):
    def wrapper(view_func):
        def inner(request, *args, **kwargs):
            data = {}
            if request.method == 'POST':
                try:
                    data = json.loads(request.body) if request.body else {}
                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Invalid JSON body'}, status=400)
                
            print("✅ JSON recibido en decorador:", data)    
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return JsonResponse({'error': 'Missing required fields'}, status=400)
            request.json_data = data
            return view_func(request, *args, **kwargs)

        return inner

    return wrapper







def auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Token '):
            token_str = auth_header[len('Token '):].strip()
        elif auth_header.startswith('Bearer '):
            token_str = auth_header[len('Bearer '):].strip()
        else:
            return JsonResponse({'error': 'Invalid authentication header'}, status=400)

        try:
            token = Token.objects.get(key=token_str)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

        request.user = token.user
        return view_func(request, *args, **kwargs)
    return wrapper
