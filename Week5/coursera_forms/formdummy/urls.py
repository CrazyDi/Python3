from django.urls import path

from . import views

urlpatterns = [
    path('', views.FormProductView.as_view()),
]