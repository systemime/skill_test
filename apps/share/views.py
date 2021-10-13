from asgiref.sync import sync_to_async
from django.http import HttpResponse
from django.shortcuts import render  # noqa

from .models import Country

# Create your views here.


def func():
    cc: Country = Country.objects.last()
    cc.is_remove = False
    cc.save()


async def test(request):

    sync_to_async(func)()
    return HttpResponse("ok")


def tests(request):
    cc: Country = Country.objects.get(id=1)
    cc.is_remove = False
    cc.save()
    return HttpResponse("ok")
