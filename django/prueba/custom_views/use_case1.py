import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from prueba.views import require_post_params, cors_response, execute_query

@require_http_methods(["GET", "OPTIONS"])
def test_get(request):
    ret = execute_query('| inputlookup "traffic_violations.csv" | head 10')
    context = {"Test": "Example get", "ret": ret}
    return cors_response(context)

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
@require_post_params(params=['email'])
def test_post(request):
    context = {"Test": "Example post"}
    return cors_response(context)
