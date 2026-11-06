from django.contrib.sessions.exceptions import SessionInterrupted
from django.http import HttpResponseRedirect
from django.urls import reverse

class SessionInterruptedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except SessionInterrupted:
            request.session.flush()
            return HttpResponseRedirect(reverse('users:login'))  
        return response