from django.conf import settings
from django.core.cache import cache


def client_ip(request):
    fwd = request.META.get('HTTP_X_FORWARDED_FOR')
    return fwd.split(',')[0].strip() if fwd else request.META.get('REMOTE_ADDR', 'unknown')


def hit(scope, key):
    """Cuenta un envío; devuelve True si se superó el límite."""
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
