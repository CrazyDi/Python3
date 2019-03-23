from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def echo(request):
    method = ''
    params = dict()
    if len(request.GET) > 0:
        method = 'GET'
        params = dict(request.GET)
    if len(request.POST) > 0:
        method = 'POST'
        params = dict(request.POST)
    statement = request.META.get("X-Print-Statement", "empty")
    return HttpResponse(render(request, 'echo.html', {'method': method.lower(), 'params': params, 'statement': statement}))


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
