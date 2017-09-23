from jose import jws
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_api.views import require_post_params, cors_response, execute_query, require_jwt

@require_http_methods(["GET", "OPTIONS"])
def test_get(request):
    ret = execute_query('| inputlookup geo_attr_countries.csv')
    context = {"Test": "Example get", "ret": ret}
    return cors_response(context, 200)

@csrf_exempt
@require_jwt()
@require_http_methods(["POST", "OPTIONS"])
@require_post_params(params=['email'])
def test_post(request):
    ret = execute_query('| inputlookup geo_attr_countries.csv')
    context = {"Test": "Example post", "ret": ret}
    return cors_response(context, 200)
