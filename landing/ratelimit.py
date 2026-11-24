from django.conf import settings
from django.core.cache import cache


def client_ip(request):
    """IP real del visitante, sin confiar en lo que el propio cliente pueda inventar.

    - X-Real-IP lo fija el proxy de PythonAnywhere (nginx) y sobrescribe cualquier valor del cliente.
    - X-Forwarded-For: el cliente puede poner lo que quiera al inicio; el proxy añade la IP real
      al final, así que se toma la ÚLTIMA entrada, nunca la primera.
    """
    real = (request.META.get('HTTP_X_REAL_IP') or '').strip()
    if real:
        return real
    fwd = request.META.get('HTTP_X_FORWARDED_FOR')
    if fwd:
        last = fwd.split(',')[-1].strip()
        if last:
            return last
    return request.META.get('REMOTE_ADDR', 'unknown')


def hit(scope, key):
    """Cuenta un envío; devuelve True si se superó el límite (caché compartido: ver CACHES en settings)."""
    cache_key = f"rl:{scope}:{key}"
    window = settings.QUOTE_RATE_WINDOW
    cache.add(cache_key, 0, window)
    try:
        count = cache.incr(cache_key)
    except ValueError:
        cache.set(cache_key, 1, window)
        count = 1
    return count > settings.QUOTE_RATE_LIMIT


def is_limited(request, scope, email=''):
    limited = hit(scope + ':ip', client_ip(request))
    if email:
        limited = hit(scope + ':mail', email.lower()) or limited
    return limited
