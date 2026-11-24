import json
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import (
    HeroSlide,
    ProductCategory,
    Product,
    CompanyStat,
    Certification,
    QuoteRequest,
    QuoteItem,
    ContactMessage,
    validate_peruvian_document,
)
from .pdf import generate_quotation_pdf
from . import pricing, ratelimit


def server_error(request):
    """Página 500 en el idioma de la URL (/es/... = español, resto = inglés).

    Sin base de datos ni context processors: si el sitio está fallando, esto debe funcionar igual.
    """
    from django.template import loader
    lang = 'es' if request.path.startswith('/es/') or request.path == '/es' else 'en'
    html = loader.get_template('500.html').render({'lang': lang})
    return HttpResponse(html, status=500)


def request_lang(request):
    """Idioma de la página: 'es' bajo /es/..., 'en' en el resto (lo fija LocaleMiddleware)."""
    return 'en' if getattr(request, 'LANGUAGE_CODE', 'es').startswith('en') else 'es'


def index(request):
    """Página de Inicio / Home: Impacto Visual estilo Xpodeka + Productos desde SQLite3"""
    lang = request_lang(request)

    hero_slides = HeroSlide.objects.filter(is_active=True)
    categories = ProductCategory.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True).select_related('category')
    featured_products = products.filter(is_featured=True)
    if not featured_products.exists():
        featured_products = products
    stats = CompanyStat.objects.all()
    certifications = Certification.objects.all()

    context = {
        'hero_slides': hero_slides,
        'categories': categories,
        'featured_products': featured_products,
        'products': products,
        'stats': stats,
        'certifications': certifications,
        'current_lang': lang,
        'active_page': 'inicio',
    }
    return render(request, 'landing/index.html', context)


def productos_view(request):
    """Página dedicada: Catálogo Visual de Granos Andinos, Semillas y Menestras en SQLite3"""
    lang = request_lang(request)

    categories = ProductCategory.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True).select_related('category')
    certifications = Certification.objects.all()

    context = {
        'categories': categories,
        'products': products,
        'certifications': certifications,
        'current_lang': lang,
        'active_page': 'productos',
    }
    return render(request, 'landing/productos.html', context)


def cotizador_view(request):
    """Página dedicada: Mesa Inteligente de Cotizaciones B2B & Contacto"""
    lang = request_lang(request)

    categories = ProductCategory.objects.filter(is_active=True)
    products = list(Product.objects.filter(is_active=True).select_related('category'))
    # Precios por kg, formateados en el servidor (el cotizador sí los muestra; el resto de la web no)
    for p in products:
        p.price_usd_label = pricing.money(pricing.unit_price(p, 'USD'), 'USD')
        p.price_pen_label = pricing.money(pricing.unit_price(p, 'PEN'), 'PEN')

    # Producto elegido en el catálogo: /cotizador/?producto=habas-secas (slug desconocido = se ignora)
    selected_slug = request.GET.get('producto', '').strip()
    if selected_slug not in {p.slug for p in products}:
        selected_slug = ''

    context = {
        'categories': categories,
        'selected_slug': selected_slug,
        'products': products,
        'current_lang': lang,
        'active_page': 'cotizador',
    }
    return render(request, 'landing/cotizador.html', context)


def nosotros_view(request):
    """Página dedicada: Sobre Nosotros (About Us) - Única sección con narrativa histórica e infraestructura"""
    lang = request_lang(request)

    categories = ProductCategory.objects.filter(is_active=True)
    stats = CompanyStat.objects.all()
    certifications = Certification.objects.all()

    context = {
        'categories': categories,
        'stats': stats,
        'certifications': certifications,
        'current_lang': lang,
        'active_page': 'nosotros',
    }
    return render(request, 'landing/nosotros.html', context)


def calidad_view(request):
    """Página dedicada: Certificaciones Globales, Inocuidad y Sostenibilidad"""
    lang = request_lang(request)

    categories = ProductCategory.objects.filter(is_active=True)
    certifications = Certification.objects.all()

    context = {
        'categories': categories,
        'certifications': certifications,
        'current_lang': lang,
        'active_page': 'calidad',
    }
    return render(request, 'landing/calidad.html', context)


SOCIAL_DISTRICTS = ['Quinua', 'Acocro', 'Tambillo', 'Acos Vinchos', 'Morochucos']

# Procesos productivos de la quinua (título ES, título EN); foto: static/images/social/etapa-NN.webp
QUINOA_STAGES = [
    ('Preparación y siembra de la Quinua', 'Quinoa land preparation and sowing'),
    ('Pos emergencia de la Quinua', 'Quinoa post-emergence'),
    ('Desarrollo vegetativo de la Quinua', 'Quinoa vegetative growth'),
    ('Desarrollo reproductivo de la Quinua', 'Quinoa reproductive growth'),
    ('Madurez de cosecha de la Quinua', 'Quinoa harvest maturity'),
    ('Cosecha de la Quinua (corte)', 'Quinoa harvest (cutting)'),
    ('Cosecha de la Quinua (trilla)', 'Quinoa harvest (threshing)'),
    ('Cosecha de la Quinua (zarandeo)', 'Quinoa harvest (sieving)'),
    ('Cosecha de la Quinua (ventilado)', 'Quinoa harvest (winnowing)'),
    ('Cosecha de la Quinua (secado)', 'Quinoa harvest (drying)'),
]


def social_view(request):
    """Página Social: capacitación a productores de Ayacucho y las 10 etapas del proceso de la quinua"""
    lang = request_lang(request)
    context = {
        'categories': ProductCategory.objects.filter(is_active=True),
        'districts': SOCIAL_DISTRICTS,
        'stages': [
            {'n': i, 'image': f'images/social/etapa-{i:02d}.webp', 'es': es, 'en': en}
            for i, (es, en) in enumerate(QUINOA_STAGES, start=1)
        ],
        'current_lang': lang,
        'active_page': 'social',
    }
    return render(request, 'landing/social.html', context)


def quote_pdf(request, token):
    """Proforma PDF; se accede solo con el código aleatorio de la cotización."""
    quote = get_object_or_404(QuoteRequest, public_token=token)
    pdf_content = generate_quotation_pdf(quote)

    response = HttpResponse(pdf_content, content_type='application/pdf')
    code = f"COT-{quote.id:04d}"
    response['Content-Disposition'] = f'inline; filename="Cotizacion_AgroSurLatino_{code}.pdf"'
    response['X-Robots-Tag'] = 'noindex'
    return response


def _msg(lang, es, en):
    return es if lang == 'es' else en


def _clean_items(raw_items, client_type, lang):
    """Valida ítems y calcula montos en el servidor. Devuelve (items, currency) o lanza ValueError(msg)."""
    if isinstance(raw_items, str):
        try:
            raw_items = json.loads(raw_items)
        except ValueError:
            raw_items = []
    if not isinstance(raw_items, list) or not raw_items:
        raise ValueError(_msg(lang, 'Seleccione al menos un producto para cotizar.', 'Please select at least one product to quote.'))
    if len(raw_items) > 50:
        raise ValueError(_msg(lang, 'Demasiados productos en una sola cotización.', 'Too many products in a single quotation.'))

    currency = pricing.currency_for(client_type)
    units_ok = pricing.allowed_units(client_type)
    clean, seen = [], set()
    for it in raw_items:
        if not isinstance(it, dict):
            raise ValueError(_msg(lang, 'Producto inválido.', 'Invalid product.'))
        try:
            product = Product.objects.get(id=int(it.get('product_id')), is_active=True)
        except (TypeError, ValueError, Product.DoesNotExist):
            raise ValueError(_msg(lang, 'Uno de los productos seleccionados no existe.', 'One of the selected products does not exist.'))
        if product.id in seen:
            raise ValueError(_msg(lang, 'Producto repetido en la cotización.', 'Duplicate product in the quotation.'))
        seen.add(product.id)

        unit = it.get('unit')
        if unit not in units_ok:
            raise ValueError(_msg(lang, 'Unidad no disponible para este tipo de cliente.', 'Unit not available for this client type.'))
        qty = pricing.parse_quantity(it.get('quantity'))
        if qty is None or qty > pricing.MAX_QTY[unit]:
            raise ValueError(_msg(
                lang,
                f'La cantidad debe ser mayor a 0 y no exceder {pricing.MAX_QTY[unit]:g}.',
                f'Quantity must be greater than 0 and not exceed {pricing.MAX_QTY[unit]:g}.',
            ))
        clean.append((product, qty, unit, pricing.compute_subtotal(product, qty, unit, currency)))
    return clean, currency


@require_POST
def quote_estimate(request):
    """Estimación en vivo para el cotizador (el precio unitario no se publica en el HTML)."""
    try:
        data = json.loads(request.body or b'{}')
        if not isinstance(data, dict):
            raise ValueError('Solicitud inválida.')
        client_type = data.get('client_type', 'JURIDICA_RUC')
        lang = 'en' if data.get('lang') == 'en' else 'es'
        items, currency = _clean_items(data.get('items', []), client_type, lang)
    except ValueError as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({
        'success': True,
        'currency': currency,
        'items': [
            {
                'product_id': p.id,
                'subtotal': pricing.money(sub, currency),
                # Nombre y cantidad en el idioma de la página (resumen "1 × 25 kg bag")
                'name': pricing.product_name(p, lang),
                'label': pricing.format_quantity(q, u, lang),
            }
            for p, q, u, sub in items
        ],
        'total': pricing.money(sum(sub for *_, sub in items), currency),
    })


@require_POST
def submit_quote(request):
    """
    Endpoint para procesar cotizaciones según tipo de cliente:
    - Persona Natural (DNI)
    - Persona Natural con Negocio (RUC 10)
    - Persona Jurídica / Empresa (RUC 20)
    - Cliente Extranjero (Tax ID / VAT)
    """
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body or b'{}')
        else:
            data = request.POST
        if not hasattr(data, 'get'):
            return JsonResponse({'success': False, 'message': 'Solicitud inválida.'}, status=400)

        client_type = _text(data, 'client_type', 20, 'JURIDICA_RUC')
        document_number = _text(data, 'document_number', 50)
        legal_name = _text(data, 'legal_name', 160)
        contact_name = _text(data, 'contact_name', 120)
        country = _text(data, 'country', 100, 'Perú')
        email = _text(data, 'email', 254)
        phone = _text(data, 'phone', 50)
        incoterm = _text(data, 'incoterm', 10, 'FOB')
        destination_port = _text(data, 'destination_port', 120)
        notes = _text(data, 'notes', 2000)
        lang = 'en' if data.get('lang') == 'en' else 'es'

        if client_type not in dict(QuoteRequest.CLIENT_TYPE_CHOICES):
            return JsonResponse({'success': False, 'message': _msg(lang, 'Tipo de cliente inválido.', 'Invalid client type.')}, status=400)
        if _is_honeypot_filled(data):  # honeypot: los bots lo rellenan
            return JsonResponse({'success': True, 'message': 'OK'})
        if not legal_name or not document_number or not email or not contact_name:
            msg = 'Por favor complete todos los datos requeridos (Nombre/Razón Social, N° Documento, Contacto y Correo).' if lang == 'es' else 'Please complete all required fields (Company Name, Document/Tax ID, Contact Person, and Email).'
            return JsonResponse({'success': False, 'message': msg}, status=400)

        # Validación estricta según Ley de RUCs de Perú / Internacional
        try:
            validate_peruvian_document(client_type, document_number, lang)
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': e.messages[0]}, status=400)

        if client_type == 'EXTRANJERO' and (not country or country.lower() in ['perú', 'peru']):
            msg = 'Para clientes internacionales, por favor especifique el país de destino/residencia.' if lang == 'es' else 'For international clients, please specify your destination country.'
            return JsonResponse({'success': False, 'message': msg}, status=400)

        if pricing.is_peru_client(client_type):
            # Cotización en Perú (RUC 20, RUC 10, DNI): sin Incoterm ni puerto
            incoterm, destination_port = '', ''
            if not country:
                country = 'Perú'
        elif incoterm not in dict(QuoteRequest.INCOTERM_CHOICES):
            incoterm = 'FOB'
        if not _valid_email(email):
            return JsonResponse({'success': False, 'message': _msg(lang, 'Ingrese un correo válido.', 'Please enter a valid email.')}, status=400)

        try:
            items, currency = _clean_items(data.get('items', []), client_type, lang)
        except ValueError as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

        # El límite solo cuenta envíos válidos: un cliente que corrige errores no queda bloqueado
        if ratelimit.is_limited(request, 'quote', email):
            return JsonResponse({'success': False, 'message': _msg(
                lang,
                'Has enviado demasiadas cotizaciones. Inténtalo de nuevo en una hora o escríbenos por correo.',
                'Too many quotations sent. Please try again in an hour or email us.')}, status=429)

        with transaction.atomic():
            quote = QuoteRequest.objects.create(
                client_type=client_type,
                document_number=document_number,
                legal_name=legal_name,
                contact_name=contact_name,
                country=country,
                email=email,
                phone=phone,
                incoterm=incoterm,
                destination_port=destination_port,
                notes=notes,
                currency=currency,
                lang=lang,
            )
            for product, qty, unit, subtotal in items:
                QuoteItem.objects.create(
                    quote_request=quote,
                    product=product,
                    quantity=qty,
                    unit=unit,
                    estimated_subtotal_usd=subtotal,
                )

        quote_code = f"COT-{quote.id:04d}"
        pdf_url = reverse('landing:quote_pdf', args=[quote.public_token])

        success_msg = _msg(
            lang,
            f"¡Cotización {quote_code} generada exitosamente! Se ha notificado a Agro Sur Latino S.A.C.",
            f"Quotation {quote_code} generated successfully! Agro Sur Latino's Export Desk has been notified.",
        )

        return JsonResponse({
            'success': True,
            'quote_id': quote.id,
            'quote_code': quote_code,
            'pdf_url': pdf_url,
            'message': success_msg,
        })

    except (ValueError, AttributeError):
        return JsonResponse({'success': False, 'message': 'Solicitud inválida.'}, status=400)
    except Exception:
        import logging
        logging.getLogger(__name__).exception('Error en submit_quote')
        return JsonResponse({
            'success': False,
            'message': 'No pudimos procesar la cotización. Inténtalo nuevamente o escríbenos por correo.'
        }, status=500)


def _text(data, key, max_len, default=''):
    """Campo de texto del formulario: siempre str, sin espacios extremos y con largo máximo."""
    value = data.get(key, default)
    if value is None or isinstance(value, bool):
        value = ''
    elif not isinstance(value, str):
        value = str(value) if isinstance(value, (int, float)) else ''
    return value.strip()[:max_len]


def _is_honeypot_filled(data):
    """Devuelve True si un bot llenó el campo trampa `website`."""
    val = data.get('website')
    if isinstance(val, str):
        return bool(val.strip())
    return bool(val)


def _valid_email(email):
    """Valida formato y largo máximo estándar de correo electrónico."""
    if not email or len(email) > 254:
        return False
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


@require_POST
def submit_contact(request):
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
    except ValueError:
        data = None
    if not hasattr(data, 'get'):
        return JsonResponse({'success': False, 'message': 'Solicitud inválida.'}, status=400)

    lang = 'en' if data.get('lang') == 'en' else 'es'
    if _is_honeypot_filled(data):  # honeypot
        return JsonResponse({'success': True, 'message': 'OK'})

    full_name = _text(data, 'full_name', 150)
    company = _text(data, 'company', 150)
    country = _text(data, 'country', 100)
    email = _text(data, 'email', 254)
    phone = _text(data, 'phone', 50)
    product_interest = _text(data, 'product_interest', 100)
    message = _text(data, 'message', 5000)

    if not full_name or not email or not company:
        return JsonResponse({
            'success': False,
            'message': _msg(lang, 'Por favor completa los campos requeridos (Nombre, Empresa y Correo).', 'Please complete the required fields (Name, Company and Email).')
        }, status=400)
    if not _valid_email(email):
        return JsonResponse({'success': False, 'message': _msg(lang, 'Ingrese un correo válido.', 'Please enter a valid email.')}, status=400)

    # El límite solo cuenta envíos válidos
    if ratelimit.is_limited(request, 'contact', email):
        return JsonResponse({'success': False, 'message': _msg(
            lang,
            'Demasiados envíos. Inténtalo más tarde o escríbenos por correo.',
            'Too many submissions. Please try again later or email us.')}, status=429)

    ContactMessage.objects.create(
        full_name=full_name,
        company=company,
        country=country or 'Perú / Internacional',
        email=email,
        phone=phone,
        product_interest=product_interest,
        message=message
    )

    return JsonResponse({
        'success': True,
        'message': _msg(
            lang,
            f'¡Gracias {full_name}! Hemos recibido tu mensaje en Agro Sur Latino S.A.C. Te responderemos a la brevedad.',
            f'Thank you {full_name}! We have received your message at Agro Sur Latino S.A.C. We will get back to you shortly.',
        )
    })
