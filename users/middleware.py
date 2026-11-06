import logging
from django.contrib.sessions.exceptions import SessionInterrupted
from django.http import HttpResponseRedirect
from django.urls import reverse

logger = logging.getLogger(__name__)


class SessionInterruptedMiddleware:
    """
    Catches SessionInterrupted exceptions that occur when a session is deleted
    mid-request (e.g. during Google OAuth callback). Must be placed AFTER
    SessionMiddleware in MIDDLEWARE so it wraps it and can intercept the
    exception raised in SessionMiddleware.process_response().
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except SessionInterrupted:
            logger.warning(
                "SessionInterrupted caught for %s — flushing session and redirecting to login.",
                request.path,
            )
            try:
                request.session.flush()
            except Exception:
                pass
            return HttpResponseRedirect(reverse('users:login'))
        return response

    def process_exception(self, request, exception):
        """
        Secondary safety net: catches SessionInterrupted if it surfaces as an
        unhandled exception rather than propagating through __call__.
        """
        if isinstance(exception, SessionInterrupted):
            logger.warning(
                "SessionInterrupted (process_exception) for %s — redirecting to login.",
                request.path,
            )
            try:
                request.session.flush()
            except Exception:
                pass
            return HttpResponseRedirect(reverse('users:login'))
        return None
