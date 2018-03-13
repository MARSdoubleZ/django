from django.conf import settings
from django.utils import translation

class AdminLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        #把界面语言设置成为中文
        if request.path.startswith('/'):

            request.LANG = getattr(settings, 'ADMIN_LANGUAGE_CODE',
                                   settings.LANGUAGE_CODE)
            translation.activate(request.LANG)
            request.LANGUAGE_CODE = request.LANG

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
