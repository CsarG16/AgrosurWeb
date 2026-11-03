import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
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


def get_products_data(products):
    return [
        {
            'id': p.id,
            'name': p.name,
            'name_en': p.name_en or p.name,
            'category': p.category.name if p.category else 'Granos y Semillas',
            'category_en': (p.category.name_en or p.category.name) if p.category else 'Grains & Seeds',
            'category_slug': p.category.slug if p.category else 'granos',
            'modality': p.modality_label_es,
            'modality_en': p.modality_label_en,
            'variety': p.variety,
            'origin': p.origin,
            'origin_en': p.origin_en,
            'season': p.season,
            'season_en': p.season_en,
            'packing_specs': p.packing_specs,
            'packing_specs_en': p.packing_specs_en,
            'price_fob': float(p.ref_price_fob_usd),
            'price_unit': p.price_unit,
            'min_order': p.min_order,
            'min_order_en': p.min_order_en,
            'image': p.get_image,
        }
        for p in products
    ]


def index(request):
    """Página de Inicio / Home: Impacto Visual estilo Xpodeka + Productos desde SQLite3"""
    lang = request.GET.get('lang', 'es')
    if lang not in ['es', 'en']:
        lang = 'es'

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
        'products_json': json.dumps(get_products_data(products)),
        'stats': stats,
        'certifications': certifications,
        'current_lang': lang,
        'active_page': 'inicio',
    }
    return render(request, 'landing/index.html', context)


def productos_view(request):
    """Página dedicada: Catálogo Visual de Granos Andinos, Semillas y Menestras en SQLite3"""
    lang = request.GET.get('lang', 'es')
    if lang not in ['es', 'en']:
        lang = 'es'

    categories = ProductCategory.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True).select_related('category')
    certifications = Certification.objects.all()

    context = {
        'categories': categories,
        'products': products,
        'products_json': json.dumps(get_products_data(products)),
        'certifications': certifications,
        'current_lang': lang,
        'active_page': 'productos',
    }
    return render(request, 'landing/productos.html', context)


def cotizador_view(request):
    """Página dedicada: Mesa Inteligente de Cotizaciones B2B & Contacto"""
    lang = request.GET.get('lang', 'es')
    if lang not in ['es', 'en']:
        lang = 'es'

    categories = ProductCategory.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True).select_related('category')

    context = {
        'categories': categories,
        'products': products,
        'products_json': json.dumps(get_products_data(products)),
        'current_lang': lang,
        'active_page': 'cotizador',
    }
    return render(request, 'landing/cotizador.html', context)


def nosotros_view(request):
    """Página dedicada: Sobre Nosotros (About Us) - Única sección con narrativa histórica e infraestructura"""
    lang = request.GET.get('lang', 'es')
    if lang not in ['es', 'en']:
        lang = 'es'

    stats = CompanyStat.objects.all()
    certifications = Certification.objects.all()

    context = {
        'stats': stats,
        'certifications': certifications,
        'current_lang': lang,
        'active_page': 'nosotros',
    }
    return render(request, 'landing/nosotros.html', context)


def calidad_view(request):
    """Página dedicada: Certificaciones Globales, Inocuidad y Sostenibilidad"""
    lang = request.GET.get('lang', 'es')
    if lang not in ['es', 'en']:
        lang = 'es'

    certifications = Certification.objects.all()

    context = {
        'certifications': certifications,
        'current_lang': lang,
        'active_page': 'calidad',
    }
    return render(request, 'landing/calidad.html', context)


def quote_pdf(request, quote_id):
    """Generación y descarga de la Proforma de Cotización en PDF con ReportLab"""
    quote = get_object_or_404(QuoteRequest, id=quote_id)
    pdf_content = generate_quotation_pdf(quote)

    response = HttpResponse(pdf_content, content_type='application/pdf')
    code = f"COT-{quote.id:04d}"
    response['Content-Disposition'] = f'inline; filename="Cotizacion_AgroSurLatino_{code}.pdf"'
    return response


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
            data = json.loads(request.body)
        else:
            data = request.POST

        client_type = data.get('client_type', 'JURIDICA_RUC')
        document_number = data.get('document_number', '').strip()
        legal_name = data.get('legal_name', '').strip()
        contact_name = data.get('contact_name', '').strip()
        country = data.get('country', 'Perú').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        incoterm = data.get('incoterm', 'FOB')
        destination_port = data.get('destination_port', '').strip()
        notes = data.get('notes', '').strip()
        lang = data.get('lang', 'es')

        if not legal_name or not document_number or not email or not contact_name:
            msg = 'Por favor complete todos los datos requeridos (Nombre/Razón Social, N° Documento, Contacto y Correo).' if lang == 'es' else 'Please complete all required fields (Company Name, Document/Tax ID, Contact Person, and Email).'
            return JsonResponse({'success': False, 'message': msg}, status=400)

        # Validación estricta según Ley de RUCs de Perú / Internacional
        try:
            validate_peruvian_document(client_type, document_number)
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': str(e.message)}, status=400)

        if client_type == 'EXTRANJERO' and (not country or country.lower() in ['perú', 'peru']):
            msg = 'Para clientes internacionales, por favor especifique el país de destino/residencia.' if lang == 'es' else 'For international clients, please specify your destination country.'
            return JsonResponse({'success': False, 'message': msg}, status=400)

        # Crear Cotización
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
        )

        # Procesar ítems cotizados
        items = data.get('items', [])
        if isinstance(items, str):
            items = json.loads(items)

        total_estimated = 0
        if items:
            for it in items:
                product_id = it.get('product_id')
                qty = float(it.get('quantity', 1))
                unit = it.get('unit', 'CONTENEDOR_40')
                subtotal = it.get('subtotal')
                try:
                    product = Product.objects.get(id=product_id)
                    QuoteItem.objects.create(
                        quote_request=quote,
                        product=product,
                        quantity=qty,
                        unit=unit,
                        estimated_subtotal_usd=subtotal if subtotal else None
                    )
                    if subtotal:
                        total_estimated += float(subtotal)
                except Product.DoesNotExist:
                    continue

        quote_code = f"COT-{quote.id:04d}"
        pdf_url = f"/cotizacion/{quote.id}/pdf/"

        if lang == 'es':
            success_msg = f"¡Cotización {quote_code} generada exitosamente! Se ha notificado a Agro Sur Latino S.A.C."
        else:
            success_msg = f"Quotation {quote_code} generated successfully! Agro Sur Latino's Export Desk has been notified."

        return JsonResponse({
            'success': True,
            'quote_id': quote.id,
            'quote_code': quote_code,
            'pdf_url': pdf_url,
            'message': success_msg,
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Error al procesar cotización: {str(e)}"
        }, status=500)


@require_POST
def submit_contact(request):
    if request.content_type == 'application/json':
        data = json.loads(request.body)
    else:
        data = request.POST

    full_name = data.get('full_name', '').strip()
    company = data.get('company', '').strip()
    country = data.get('country', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    product_interest = data.get('product_interest', '').strip()
    message = data.get('message', '').strip()

    if not full_name or not email or not company:
        return JsonResponse({
            'success': False,
            'message': 'Por favor completa los campos requeridos (Nombre, Empresa y Correo).'
        }, status=400)

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
        'message': f'¡Gracias {full_name}! Hemos recibido tu mensaje en Agro Sur Latino S.A.C. Te responderemos a la brevedad.'
    })
