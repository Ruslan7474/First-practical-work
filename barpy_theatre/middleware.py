from barpy_theatre.i18n import normalize_lang


class SiteLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_lang = request.session.get("site_lang")
        cookie_lang = request.COOKIES.get("site_lang")
        request.site_lang = normalize_lang(session_lang or cookie_lang or "ru")
        response = self.get_response(request)
        return response
