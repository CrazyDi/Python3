from django.conf.urls import url

from template.views import echo, filters, extend

urlpatterns = [
    url(r'^echo/$', echo, name='echo'),
    url(r'^filters/$', filters),
    url(r'^extend/$', extend),
]
