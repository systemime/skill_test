import asyncio
import time

from django.utils.decorators import sync_and_async_middleware


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print(1)
        response = self.get_response(request)
        print(2)
        # Code to be executed for each request/response after
        # the view is called.

        return response


def add_elapsed_time(response, start):
    response.__setattr__("elapsed", time.perf_counter() - start)
    return response


@sync_and_async_middleware
def timing_middleware(get_response):
    if asyncio.iscoroutinefunction(get_response):

        async def middleware(request):
            start = time.perf_counter()
            response = await get_response(request)
            response = add_elapsed_time(response, start)
            return response

    else:

        def middleware(request):
            start = time.perf_counter()
            response = get_response(request)
            response = add_elapsed_time(response, start)
            return response

    return middleware
