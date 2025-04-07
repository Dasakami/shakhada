class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        theme = request.COOKIES.get('theme', 'light')
        request.theme = theme  # Передаём тему в шаблон через request
        response = self.get_response(request)
        return response
