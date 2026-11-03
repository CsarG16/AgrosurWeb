import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT


def generate_quotation_pdf(quote):
    """
    Genera un documento PDF profesional y corporativo de la cotización B2B de Agrosur.
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

    # Colores corporativos suaves de Agrosur
    c_primary = colors.HexColor('#223120')      # Dark olive slate
    c_accent = colors.HexColor('#587c52')       # Natural leaf green
    c_subtle = colors.HexColor('#759b6e')       # Eucalyptus
    c_bg_light = colors.HexColor('#f6f8f5')     # Soft sage background
    c_border = colors.HexColor('#d7e4d3')       # Border tone
    c_dark = colors.HexColor('#1f2937')         # Text dark
    c_muted = colors.HexColor('#6b7280')        # Text muted

    # Estilos de texto
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

    # 1. Cabecera Corporativa
    code = f"COT-{quote.id:04d}"
    date_str = quote.created_at.strftime('%d/%m/%Y %H:%M') if hasattr(quote, 'created_at') and quote.created_at else datetime.now().strftime('%d/%m/%Y')

    header_left = [
        Paragraph("<b>AGROSUR S.A.C.</b>", title_style),
        Paragraph("RUC 20608945123 • SUNAT Perú", subtitle_style),
        Paragraph("Agroexportación de Frutos Frescos & Superfoods de Origen", subtitle_style),
        Paragraph("Valles de Producción: Ica • Piura • Olmos | Lima - Perú", subtitle_style),
    ]

    header_right = [
        Paragraph(f"<b>PROFORMA DE EXPORTACIÓN</b>", right_bold),
        Paragraph(f"<b>N° Documento:</b> {code}", right_style),
        Paragraph(f"<b>Fecha:</b> {date_str}", right_style),
        Paragraph(f"<b>Incoterm Solicitado:</b> {quote.incoterm}", right_style),
    ]

    header_table = Table([[header_left, header_right]], colWidths=[310, 222])
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
            Paragraph("<b>Puerto / Aeropuerto:</b>", body_style),
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

    # 3. Frutos y Volúmenes Cotizados
    story.append(Paragraph("DETALLE DE FRUTOS Y VOLÚMENES ESTIMADOS", heading_style))
    story.append(Spacer(1, 6))

    unit_labels = {
        'CONTENEDOR_40': 'Contenedor 40ft (~21 TM)',
        'PALLET': 'Pallets Exportación',
        'TONELADAS': 'Toneladas Métricas (TM)',
        'CAJAS': 'Cajas Master',
    }

    items_data = [
        [
            Paragraph("<b>Ítem / Fruto</b>", body_bold),
            Paragraph("<b>Variedad / Origen</b>", body_bold),
            Paragraph("<b>Cantidad & Unidad</b>", body_bold),
            Paragraph("<b>Ref. FOB Unit.</b>", right_bold),
            Paragraph("<b>Subtotal Estimado</b>", right_bold),
        ]
    ]

    total_est = 0
    items = quote.items.all()
    if items:
        for it in items:
            p = it.product
            qty = it.quantity
            unit_name = unit_labels.get(it.unit, it.unit)
            unit_price = f"${p.ref_price_fob_usd:.2f}/{p.price_unit}" if p else "Consultar"
            subtotal_val = it.estimated_subtotal_usd or 0
            total_est += float(subtotal_val)
            subtotal_str = f"${subtotal_val:,.2f} USD" if subtotal_val else "Por cotizar"

            items_data.append([
                Paragraph(p.name if p else "Fruto fresco", body_bold),
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
            Paragraph("$0.00 USD", right_style),
        ])

    # Fila de Totales
    items_data.append([
        Paragraph("<b>TOTAL ESTIMADO DE REFERENCIA (FOB USD):</b>", body_bold),
        "",
        "",
        "",
        Paragraph(f"<b>${total_est:,.2f} USD</b>", right_bold),
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
        ('SPAN', (0, -1), (3, -1)),  # Fusionar celda de total
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

    # 5. Términos y Garantías de Exportación
    story.append(Paragraph("CONDICIONES COMERCIALES & ESTÁNDARES FITOSANITARIOS", heading_style))
    story.append(Spacer(1, 4))
    terms_text = (
        "1. <b>Validez de la oferta:</b> 7 días hábiles a partir de la fecha de emisión, sujeta a confirmación de calibres y disponibilidad de espacio naviero reefer.<br/>"
        "2. <b>Cadena de frío continua:</b> Cámaras frigoríficas con monitoreo térmico satelital continuo desde packing hasta puerto de destino.<br/>"
        "3. <b>Certificaciones incluidas:</b> GlobalG.A.P., HACCP, BRCGS Food Safety e inspección fitosanitaria oficial SENASA Perú.<br/>"
        "4. <b>Mesa comercial:</b> exportaciones@agrosur.pe • +51 (1) 748-2900 • Lima, Perú."
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
    story.append(Paragraph("<i>Agrosur S.A.C. — Agroexportación de Excelencia desde el Perú para el Mundo.</i>", ParagraphStyle(
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
