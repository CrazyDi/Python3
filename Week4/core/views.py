from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html')


def topic_details(request, pk):
    return render(request, 'core/topic_details.html')
