from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import re


@csrf_exempt
def simple_route(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    else:
        return HttpResponseNotAllowed('GET')


def slug_route(request, slug):
    return HttpResponse(slug)


def sum_route(request, a, b):
    return HttpResponse(int(a) + int(b))


def sum_get_method(request):
    if request.method == 'GET':
        a = request.GET.get('a', '')
        b = request.GET.get('b', '')
        try:
            return HttpResponse(int(a) + int(b))
        except ValueError:
            return HttpResponse(status=400)
    return HttpResponseNotAllowed('GET')


def sum_post_method(request):
    if request.method == 'POST':
        a = request.POST.get('a', '')
        b = request.POST.get('b', '')
        try:
            return HttpResponse(int(a) + int(b))
        except ValueError:
            return HttpResponse(status=400)
    return HttpResponseNotAllowed('POST')
