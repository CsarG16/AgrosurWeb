import io
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.utils import timezone

from . import pricing
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

COMPANY_ADDRESS = settings.COMPANY_ADDRESS
COMPANY_EMAIL = settings.COMPANY_EMAIL


def generate_quotation_pdf(quote):
    """
    Genera un documento PDF profesional y corporativo de la cotización B2B de Agro Sur Latino S.A.C.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Colores corporativos de Agro Sur Latino S.A.C.
    c_primary = colors.HexColor('#223120')
    c_accent = colors.HexColor('#a63a2b')       # Terracota / Andino Xpodeka accent
    c_bg_light = colors.HexColor('#faf8f5')
    c_border = colors.HexColor('#e5dec9')
    c_dark = colors.HexColor('#1f2937')
    c_muted = colors.HexColor('#6b7280')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=c_primary,
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=c_muted,
    )
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_primary,
    )
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=c_dark,
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold',
    )
    right_style = ParagraphStyle(
        'RightText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        alignment=TA_RIGHT,
        textColor=c_dark,
    )
    right_bold = ParagraphStyle(
        'RightBold',
        parent=right_style,
        fontName='Helvetica-Bold',
        textColor=c_primary,
    )

    # 1. Cabecera Corporativa Real de Agro Sur Latino S.A.C.
    code = f"COT-{quote.id:04d}"
    created = timezone.localtime(quote.created_at) if quote.created_at else timezone.localtime()
    date_str = created.strftime('%d/%m/%Y %H:%M')
    currency = quote.currency

    header_left = [
        Paragraph("<b>AGRO SUR LATINO S.A.C.</b>", title_style),
        Paragraph("RUC 20517805662 • Lima, Perú", subtitle_style),
        Paragraph("Granos Andinos, Semillas y Menestras (Orgánicos y Convencionales)", subtitle_style),
        Paragraph(f"{COMPANY_ADDRESS} | {COMPANY_EMAIL}", subtitle_style),
    ]

    header_right = [
        Paragraph("<b>PROFORMA DE EXPORTACIÓN</b>", right_bold),
        Paragraph(f"<b>N° Documento:</b> {code}", right_style),
        Paragraph(f"<b>Fecha:</b> {date_str}", right_style),
        Paragraph(f"<b>Incoterm Solicitado:</b> {quote.incoterm}", right_style),
    ]

    logo_path = settings.BASE_DIR / 'static' / 'images' / 'agrosurlogo.png'
    if logo_path.exists():
        try:
            logo = Image(str(logo_path), width=110, height=110 * 0.35)
            logo.hAlign = 'LEFT'
            logo._restrictSize(110, 60)
            header_left.insert(0, logo)
        except Exception:
            pass

    header_table = Table([[header_left, header_right]], colWidths=[320, 212])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(header_table)

    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=14))

    # 2. Datos del Cliente / Importador
    story.append(Paragraph("DATOS DEL CLIENTE / IMPORTADOR", heading_style))
    story.append(Spacer(1, 6))

    client_type_labels = {
        'JURIDICA_RUC': 'Persona Jurídica / Empresa (RUC 20)',
        'NATURAL_RUC': 'Persona Natural con Negocio (RUC 10)',
        'NATURAL_DNI': 'Persona Natural (DNI Perú)',
        'EXTRANJERO': 'Importador Internacional / Tax ID',
    }
    client_type_text = client_type_labels.get(quote.client_type, quote.client_type)

    client_info = [
        [
            Paragraph("<b>Razón Social / Nombre:</b>", body_style),
            Paragraph(quote.legal_name, body_bold),
            Paragraph("<b>Tipo de Cliente:</b>", body_style),
            Paragraph(client_type_text, body_style),
        ],
        [
            Paragraph("<b>N° Documento / Tax ID:</b>", body_style),
            Paragraph(quote.document_number, body_bold),
            Paragraph("<b>País de Destino:</b>", body_style),
            Paragraph(quote.country, body_style),
        ],
        [
            Paragraph("<b>Persona de Contacto:</b>", body_style),
            Paragraph(quote.contact_name, body_style),
            Paragraph("<b>Puerto / Destino:</b>", body_style),
            Paragraph(quote.destination_port or "Callao / Por confirmar", body_style),
        ],
        [
            Paragraph("<b>Correo Corporativo:</b>", body_style),
            Paragraph(quote.email, body_style),
            Paragraph("<b>Teléfono / WhatsApp:</b>", body_style),
            Paragraph(quote.phone, body_style),
        ],
    ]

    client_table = Table(client_info, colWidths=[120, 150, 110, 152])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(client_table)
    story.append(Spacer(1, 16))

    # 3. Granos, Semillas y Volúmenes Cotizados
    story.append(Paragraph("DETALLE DE PRODUCTOS Y VOLÚMENES ESTIMADOS", heading_style))
    story.append(Spacer(1, 6))

    unit_labels = {
        'CONTENEDOR_FCL': 'Contenedor FCL (~20 TM)',
        'PALLET': 'Pallets (1 TM)',
        'TONELADAS': 'Toneladas Métricas (TM)',
        'SACOS_25KG': 'Sacos 25 kg',
        'KILOS': 'Kilos',
    }

    items_data = [
        [
            Paragraph("<b>Producto / Grano</b>", body_bold),
            Paragraph("<b>Modalidad & Origen</b>", body_bold),
            Paragraph("<b>Cantidad & Unidad</b>", body_bold),
            Paragraph("<b>Precio por kg</b>" if currency == "PEN" else "<b>Ref. FOB por kg</b>", right_bold),
            Paragraph("<b>Subtotal Estimado</b>", right_bold),
        ]
    ]

    total_est = Decimal('0')
    items = quote.items.select_related('product').all()
    if items:
        for it in items:
            p = it.product
            qty = it.quantity
            unit_name = unit_labels.get(it.unit, it.unit)
            unit_price = f"{pricing.money(pricing.unit_price(p, currency), currency)}/kg" if p else "Consultar"
            subtotal_val = it.estimated_subtotal_usd or Decimal('0')
            total_est += subtotal_val
            subtotal_str = pricing.money(subtotal_val, currency) if subtotal_val else "Por cotizar"

            items_data.append([
                Paragraph(p.name if p else "Grano Andino", body_bold),
                Paragraph(f"{p.variety} • {p.origin}" if p else "-", body_style),
                Paragraph(f"{qty:g} {unit_name}", body_style),
                Paragraph(unit_price, right_style),
                Paragraph(subtotal_str, right_bold),
            ])
    else:
        items_data.append([
            Paragraph("Sin ítems especificados", body_style),
            Paragraph("-", body_style),
            Paragraph("-", body_style),
            Paragraph("-", right_style),
            Paragraph(pricing.money(0, currency), right_style),
        ])

    items_data.append([
        Paragraph("<b>TOTAL ESTIMADO (S/ incluye IGV):</b>" if currency == "PEN" else "<b>TOTAL ESTIMADO DE REFERENCIA (FOB US$):</b>", body_bold),
        "",
        "",
        "",
        Paragraph(f"<b>{pricing.money(total_est, currency)}</b>", right_bold),
    ])

    items_table = Table(items_data, colWidths=[120, 130, 132, 70, 80])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('INNERGRID', (0, 0), (-1, -2), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('SPAN', (0, -1), (3, -1)),
        ('BACKGROUND', (0, -1), (-1, -1), c_bg_light),
        ('LINEABOVE', (0, -1), (-1, -1), 1, c_accent),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 14))

    # 4. Notas del Pedido si existen
    if quote.notes:
        story.append(Paragraph("NOTAS Y ESPECIFICACIONES ADICIONALES", heading_style))
        story.append(Spacer(1, 4))
        notes_p = Paragraph(quote.notes, body_style)
        notes_table = Table([[notes_p]], colWidths=[532])
        notes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
            ('BOX', (0, 0), (-1, -1), 0.5, c_border),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(notes_table)
        story.append(Spacer(1, 14))

    # 5. Condiciones Comerciales
    story.append(Paragraph("CONDICIONES COMERCIALES & CERTIFICACIONES DE CALIDAD", heading_style))
    story.append(Spacer(1, 4))
    terms_text = (
        "1. <b>Disponibilidad y Stock:</b> Abastecimiento permanente todo el año desde nuestros almacenes en Huachipa (Lima) y centros de acopio en Ayacucho.<br/>"
        "2. <b>Presentaciones:</b> Disponible en modalidades Orgánica Certificada y Convencional según requerimiento del cliente.<br/>"
        "3. <b>Certificaciones:</b> HACCP, BRC, USDA Organic, EU Organic, JAS, FDA y Certificado Fitosanitario SENASA Perú.<br/>"
        f"4. <b>Contacto Comercial:</b> {COMPANY_EMAIL} • {COMPANY_ADDRESS}, Lima, Perú."
    )
    terms_p = Paragraph(terms_text, subtitle_style)
    terms_table = Table([[terms_p]], colWidths=[532])
    terms_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(terms_table)

    story.append(Spacer(1, 20))
    story.append(Paragraph("<i>Agro Sur Latino S.A.C. — De los productores hacia el mundo.</i>", ParagraphStyle(
        'FooterNote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        alignment=TA_CENTER,
        textColor=c_muted
    )))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
