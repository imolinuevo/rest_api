# -*- coding: utf-8 -*-
import json
from django.contrib.auth.decorators import login_required
from splunkdj.decorators.render import render_to
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import available_attrs
from functools import wraps
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import splunklib.client as client
import splunklib.results as results
from django.contrib.auth import authenticate
from datetime import timedelta, date, datetime
from config import CustomConfig
from jose import jwt

def require_post_params(params):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            if request.method != "OPTIONS" and not all(param in request.POST for param in params):
                return HttpResponseBadRequest()
            return func(request, *args, **kwargs)
        return inner
    return decorator

def require_jwt():
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            authorization = request.META.get('HTTP_AUTHORIZATON', None)
            if authorization == None:
                return cors_response('JSON Web Token is required', 401)
            else:
                try:
                  decoded_token = jwt.decode(authorization, CustomConfig.JWT_SECRET_KEY, algorithms=CustomConfig.JWT_ALGORITHM)
                  is_expired = datetime.strptime(decoded_token['expirity'], '%Y/%m/%d %H:%M:%S') < datetime.now()
                  if(is_expired):
                      return cors_response('JSON Web Token expired', 401)
                except:
                  return cors_response('JSON Web Token is required', 401)
            return func(request, *args, **kwargs)
        return inner
    return decorator

def cors_response(context, status_code):
    response = HttpResponse(json.dumps(context), content_type="application/json", status=status_code)
    response["Access-Control-Allow-Origin"] = CustomConfig.CORS_URL
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response["Access-Control-Allow-Methods"] = "GET,PUT,POST,DELETE,PATCH,OPTIONS"
    return response

def execute_query(query):
    service = client.connect(
        host=CustomConfig.SPLUNK_HOST,
        port=CustomConfig.SPLUNK_PORT,
        username=CustomConfig.SPLUNK_USERNAME,
        password=CustomConfig.SPLUNK_PASSWORD
    )
    kwargs = {"exec_mode": "blocking"}
    job = service.jobs.create(query, **kwargs)
    ret = []
    for result in results.ResultsReader(job.results()):
        ret.append(result)
    job.cancel()
    return ret

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
@require_post_params(params=['username', 'password'])
def auth_jwt(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user == None:
        return cors_response('Unauthorized', 401)
    expirity = datetime.now() + timedelta(hours=CustomConfig.JWT_EXPIRATION_HOURS)
    token = jwt.encode(
        {
            'username': user.username,
            'expirity': expirity.strftime('%Y/%m/%d %H:%M:%S')
        },
        CustomConfig.JWT_SECRET_KEY,
        algorithm = CustomConfig.JWT_ALGORITHM
    )
    context = {'token': token}
    return cors_response(context, 200)

@render_to('rest_api:home.html')
@login_required
def home(request):
    return {}
