import re
from urllib.parse import quote

from django.conf import settings
from django.urls import translate_url
from django.utils import timezone, translation

from .models import Certification
from . import i18n


def _language_links(request):
    """URLs del selector ES|EN (conservan ?cat=…) y URLs absolutas sin query para canonical/hreflang."""
    full_path = request.get_full_path()
    path = request.path
    codes = [code for code, _name in settings.LANGUAGES]
    links = {code: translate_url(full_path, code) for code in codes}
    absolute = {code: request.build_absolute_uri(translate_url(path, code)) for code in codes}
    return {
        'lang_links': links,
        'hreflang_urls': absolute,
        'canonical_url': absolute.get(translation.get_language() or settings.LANGUAGE_CODE, request.build_absolute_uri(path)),
        'default_url': absolute[settings.LANGUAGE_CODE],
    }


def company(request):
    phone = settings.COMPANY_PHONE.strip()
    phone_digits = re.sub(r'\D', '', phone)
    whatsapp_digits = re.sub(r'\D', '', settings.COMPANY_WHATSAPP)
    # Una sola fuente de verdad para las certificaciones: la tabla Certification (pie, /calidad/, descripciones)
    whatsapp_text = (
        "Hello, I would like a quote for Agro Sur Latino products."
        if translation.get_language() == 'en' else
        'Hola, quisiera cotizar productos de Agro Sur Latino.'
    )
    cert_names = list(Certification.objects.values_list('name', flat=True))
    return {
        **_language_links(request),
        'company_address': settings.COMPANY_ADDRESS,
        'company_email': settings.COMPANY_EMAIL,
        'company_founded_year': settings.COMPANY_FOUNDED_YEAR,
        'company_years': timezone.localdate().year - settings.COMPANY_FOUNDED_YEAR,
        'company_maps_url': settings.COMPANY_MAPS_URL,
        # Mapa de Google embebido (sin clave de API), en el idioma de la página
        'company_map_embed_url': (
            f'https://www.google.com/maps?q={settings.COMPANY_LAT},{settings.COMPANY_LNG}'
            f'&z=16&hl={"en" if translation.get_language() == "en" else "es"}&output=embed'
        ),
        'company_phone': phone,
        'company_phone_href': f'tel:+{phone_digits}' if phone_digits else '',
        'company_whatsapp_url': (
            f"https://wa.me/{whatsapp_digits}?text={quote(whatsapp_text)}"
            if whatsapp_digits else ''
        ),
        'cert_names': cert_names,
        'cert_names_text': ', '.join(cert_names),
        'i18n_data': i18n.load(),
    }
