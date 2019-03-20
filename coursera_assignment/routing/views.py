from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re


@csrf_exempt
def simple_route(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)


def slug_route(request, slug):
    return HttpResponse(slug)


def sum_route(request, a, b):
    return HttpResponse(int(a) + int(b))


@csrf_exempt
def sum_get_method(request):
    if request.method == 'GET':
        if 'a' in request.GET and 'b' in request.GET:
            if re.match('\d', request.GET['a']) and re.match('\d', request.GET['b']):
                return HttpResponse(int(request.GET['a']) + int(request.GET['b']))

    return HttpResponse(status=400)


@csrf_exempt
def sum_post_method(request):
    if request.method == 'POST':
        if 'a' in request.POST and 'b' in request.POST:
            if re.match('\d', request.POST['a']) and re.match('\d', request.POST['b']):
                return HttpResponse(int(request.POST['a']) + int(request.POST['b']))

    return HttpResponse(status=400)

