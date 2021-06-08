import requests
import re
from django.shortcuts import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt


def middle_man(request):
    response = requests.get('https://www.pythonanywhere.com/login')
    return HttpResponse(response)


SITE_NAME = 'https://www.pythonanywhere.com'

man = requests.session()


class MiddleMan(View):
    def get(self, request):
        path = SITE_NAME + request.path
        response = man.get(path)
        return HttpResponse(change_content_src(response))

    @csrf_exempt
    def post(self, request):
        path = SITE_NAME + request.path
        data = request.POST.dict()
        response = man.post(path, data, headers=dict(Referer=path))
        return HttpResponse(change_content_src(response))


def change_content_src(response):
    pattern = b'"/static'
    repl = '"' + SITE_NAME + '/static'
    return re.sub(pattern, repl.encode(), response.content)
