from django.http import HttpResponse
from django.shortcuts import render  # noqa

# Create your views here.


async def test(request):
    return HttpResponse("ok")
