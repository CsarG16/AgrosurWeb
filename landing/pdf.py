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
    lang = quote.lang if getattr(quote, 'lang', 'es') == 'en' else 'es'
    peru = pricing.is_peru_client(quote.client_type)

    def T(es, en):
        return en if lang == 'en' else es

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
        Paragraph(T("RUC 20517805662 • Lima, Perú", "RUC 20517805662 • Lima, Peru"), subtitle_style),
        Paragraph(T("Granos Andinos, Semillas y Menestras (Orgánicos y Convencionales)", "Andean Grains, Seeds & Pulses (Organic & Conventional)"), subtitle_style),
        Paragraph(f"{COMPANY_ADDRESS} | {COMPANY_EMAIL}", subtitle_style),
    ]

    if peru:
        # Cotización para Perú (RUC 20, RUC 10, DNI): sin Incoterm ni "proforma de exportación"
        header_right = [Paragraph(T("<b>COTIZACIÓN</b>", "<b>QUOTATION</b>"), right_bold)]
    else:
        header_right = [Paragraph(T("<b>PROFORMA DE EXPORTACIÓN</b>", "<b>EXPORT PROFORMA INVOICE</b>"), right_bold)]
    header_right += [
        Paragraph(f"<b>{T('N° Documento', 'Document No.')}:</b> {code}", right_style),
        Paragraph(f"<b>{T('Fecha', 'Date')}:</b> {date_str}", right_style),
    ]
    if not peru and quote.incoterm:
        header_right.append(Paragraph(f"<b>{T('Incoterm Solicitado', 'Requested Incoterm')}:</b> {quote.incoterm}", right_style))

    logo_path = settings.BASE_DIR / 'static' / 'images' / 'agrosurlogo.png'
    if logo_path.exists():
        try:
            from PIL import Image as PILImage
            with PILImage.open(logo_path) as pil_logo:
                ratio = pil_logo.height / pil_logo.width  # conserva la proporción real del logo
            logo = Image(str(logo_path), width=130, height=130 * ratio)
            logo.hAlign = 'LEFT'
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

    # 2. Datos del cliente (en Perú: "Datos del cliente"; exportación: "cliente / importador")
    if peru:
        story.append(Paragraph(T("DATOS DEL CLIENTE", "CLIENT DETAILS"), heading_style))
    else:
        story.append(Paragraph(T("DATOS DEL CLIENTE / IMPORTADOR", "CLIENT / IMPORTER DETAILS"), heading_style))
    story.append(Spacer(1, 6))

    client_type_labels = {
        'JURIDICA_RUC': T('Persona Jurídica / Empresa (RUC 20)', 'Company (RUC 20)'),
        'NATURAL_RUC': T('Persona Natural con Negocio (RUC 10)', 'Sole proprietor (RUC 10)'),
        'NATURAL_DNI': T('Persona Natural (DNI Perú)', 'Individual (Peruvian DNI)'),
        'EXTRANJERO': T('Importador Internacional / Tax ID', 'International importer / Tax ID'),
    }
    client_type_text = client_type_labels.get(quote.client_type, quote.client_type)

    def lbl(es, en):
        return Paragraph(f"<b>{T(es, en)}:</b>", body_style)

    client_info = [
        [lbl("Razón Social / Nombre", "Company / Name"), Paragraph(quote.legal_name, body_bold),
         lbl("Tipo de Cliente", "Client Type"), Paragraph(client_type_text, body_style)],
        [lbl("N° Documento / Tax ID", "Document / Tax ID"), Paragraph(quote.document_number, body_bold),
         lbl("País" if peru else "País de Destino", "Country" if peru else "Destination Country"), Paragraph(quote.country, body_style)],
    ]
    if peru:
        client_info += [
            [lbl("Persona de Contacto", "Contact Person"), Paragraph(quote.contact_name, body_style),
             lbl("Teléfono / WhatsApp", "Phone / WhatsApp"), Paragraph(quote.phone, body_style)],
            [lbl("Correo", "Email"), Paragraph(quote.email, body_style), "", ""],
        ]
    else:
        client_info += [
            [lbl("Persona de Contacto", "Contact Person"), Paragraph(quote.contact_name, body_style),
             lbl("Puerto / Destino", "Port / Destination"), Paragraph(quote.destination_port or T("Callao / Por confirmar", "Callao / To be confirmed"), body_style)],
            [lbl("Correo Corporativo", "Corporate Email"), Paragraph(quote.email, body_style),
             lbl("Teléfono / WhatsApp", "Phone / WhatsApp"), Paragraph(quote.phone, body_style)],
        ]

    client_table = Table(client_info, colWidths=[120, 150, 110, 152])
    client_style = [
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    if peru:
        client_style.append(('SPAN', (1, 3), (3, 3)))
    client_table.setStyle(TableStyle(client_style))
    story.append(client_table)
    story.append(Spacer(1, 16))

    # 3. Granos, Semillas y Volúmenes Cotizados
    story.append(Paragraph(T("DETALLE DE PRODUCTOS Y VOLÚMENES ESTIMADOS", "PRODUCT DETAILS AND ESTIMATED VOLUMES"), heading_style))
    story.append(Spacer(1, 6))

    price_header = T("Precio por kg", "Price per kg") if currency == "PEN" else T("Ref. FOB por kg", "FOB ref. per kg")
    items_data = [
        [
            Paragraph(f"<b>{T('Producto / Grano', 'Product / Grain')}</b>", body_bold),
            Paragraph(f"<b>{T('Modalidad & Origen', 'Type & Origin')}</b>", body_bold),
            Paragraph(f"<b>{T('Cantidad & Unidad', 'Quantity & Unit')}</b>", body_bold),
            Paragraph(f"<b>{price_header}</b>", right_bold),
            Paragraph(f"<b>{T('Subtotal Estimado', 'Estimated Subtotal')}</b>", right_bold),
        ]
    ]

    total_est = Decimal('0')
    items = quote.items.select_related('product').all()
    if items:
        for it in items:
            p = it.product
            unit_price = f"{pricing.money(pricing.unit_price(p, currency), currency)}/kg" if p else T("Consultar", "Inquire")
            subtotal_val = it.estimated_subtotal_usd or Decimal('0')
            total_est += subtotal_val
            subtotal_str = pricing.money(subtotal_val, currency) if subtotal_val else T("Por cotizar", "To be quoted")
            if p and lang == 'en':
                type_origin = f"{p.modality_label_en} • {p.origin_en or p.origin}"
            else:
                type_origin = f"{p.variety} • {p.origin}" if p else "-"

            items_data.append([
                Paragraph(pricing.product_name(p, lang) if p else T("Grano Andino", "Andean Grain"), body_bold),
                Paragraph(type_origin, body_style),
                Paragraph(pricing.format_quantity(it.quantity, it.unit, lang), body_style),
                Paragraph(unit_price, right_style),
                Paragraph(subtotal_str, right_bold),
            ])
    else:
        items_data.append([
            Paragraph(T("Sin ítems especificados", "No items specified"), body_style),
            Paragraph("-", body_style),
            Paragraph("-", body_style),
            Paragraph("-", right_style),
            Paragraph(pricing.money(0, currency), right_style),
        ])

    items_data.append([
        Paragraph(
            T("<b>TOTAL ESTIMADO (S/ incluye IGV):</b>", "<b>ESTIMATED TOTAL (S/ incl. VAT):</b>") if currency == "PEN"
            else T("<b>TOTAL ESTIMADO DE REFERENCIA (FOB US$):</b>", "<b>ESTIMATED REFERENCE TOTAL (FOB US$):</b>"),
            body_bold,
        ),
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
        story.append(Paragraph(T("NOTAS Y ESPECIFICACIONES ADICIONALES", "NOTES AND ADDITIONAL SPECIFICATIONS"), heading_style))
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
    story.append(Paragraph(T("CONDICIONES COMERCIALES Y CERTIFICACIONES DE CALIDAD", "COMMERCIAL TERMS AND QUALITY CERTIFICATIONS"), heading_style))
    story.append(Spacer(1, 4))
    terms_text = T(
        "1. <b>Disponibilidad y Stock:</b> Abastecimiento permanente todo el año desde nuestros almacenes en Huachipa (Lima) y centros de acopio en Ayacucho.<br/>"
        "2. <b>Presentaciones:</b> Disponible en modalidades Orgánica Certificada y Convencional según requerimiento del cliente.<br/>"
        "3. <b>Certificaciones:</b> HACCP, BRC, USDA Organic, EU Organic, JAS, FDA y Certificado Fitosanitario SENASA Perú.<br/>"
        f"4. <b>Contacto Comercial:</b> {COMPANY_EMAIL} • {COMPANY_ADDRESS}, Lima, Perú.",
        "1. <b>Availability and stock:</b> Year-round supply from our warehouses in Huachipa (Lima) and collection centers in Ayacucho.<br/>"
        "2. <b>Presentations:</b> Available as Certified Organic and Conventional, according to the client's requirements.<br/>"
        "3. <b>Certifications:</b> HACCP, BRC, USDA Organic, EU Organic, JAS, FDA and SENASA Peru Phytosanitary Certificate.<br/>"
        f"4. <b>Sales contact:</b> {COMPANY_EMAIL} • {COMPANY_ADDRESS}, Lima, Peru.",
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
    slogan = settings.COMPANY_SLOGAN_EN if lang == 'en' else settings.COMPANY_SLOGAN
    story.append(Paragraph(f"<i>Agro Sur Latino S.A.C. — {slogan}.</i>", ParagraphStyle(
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
