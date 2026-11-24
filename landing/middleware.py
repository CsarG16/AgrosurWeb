from .i18n import translate_html


class EnglishHTMLMiddleware:
    """Envía las páginas /en/... con el texto ya traducido (para buscadores y vistas previas en redes).

    Las plantillas están escritas en español; el diccionario está en landing/i18n.json.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (
            getattr(request, 'LANGUAGE_CODE', 'es') == 'en'
            and response.get('Content-Type', '').startswith('text/html')
            and not getattr(response, 'streaming', False)
            and response.status_code == 200
        ):
            charset = response.charset or 'utf-8'
            response.content = translate_html(response.content.decode(charset)).encode(charset)
            if response.has_header('Content-Length'):
                response['Content-Length'] = str(len(response.content))
        return response
