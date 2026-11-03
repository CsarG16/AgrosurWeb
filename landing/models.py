from django.db import models
from django.core.exceptions import ValidationError
import re


def validate_peruvian_document(client_type, doc_num):
    doc_num = doc_num.strip()
    if client_type == 'NATURAL_DNI':
        if not re.match(r'^\d{8}$', doc_num):
            raise ValidationError("El DNI peruano debe contener exactamente 8 dígitos numéricos.")
    elif client_type == 'NATURAL_RUC':
        if not re.match(r'^\d{11}$', doc_num) or not (doc_num.startswith('10') or doc_num.startswith('15') or doc_num.startswith('17')):
            raise ValidationError("El RUC de Persona Natural (Ley del RUC - SUNAT) debe contener 11 dígitos e iniciar con 10.")
    elif client_type == 'JURIDICA_RUC':
        if not re.match(r'^\d{11}$', doc_num) or not doc_num.startswith('20'):
            raise ValidationError("El RUC de Persona Jurídica / Empresa (Ley del RUC - SUNAT) debe contener 11 dígitos e iniciar con 20.")
    elif client_type == 'EXTRANJERO':
        if len(doc_num) < 4:
            raise ValidationError("Ingrese un Tax ID / VAT / Registro Fiscal internacional válido.")


class HeroSlide(models.Model):
    title = models.CharField(max_length=150, verbose_name="Título Principal (ES)")
    title_en = models.CharField(max_length=150, blank=True, verbose_name="Título Principal (EN)")
    tagline = models.CharField(max_length=200, verbose_name="Subtítulo o Lema (ES)")
    tagline_en = models.CharField(max_length=200, blank=True, verbose_name="Subtítulo o Lema (EN)")
    badge = models.CharField(max_length=50, default="Perú al Mundo", verbose_name="Insignia / Etiqueta (ES)")
    badge_en = models.CharField(max_length=50, default="Peru to the World", verbose_name="Insignia / Etiqueta (EN)")
    image = models.ImageField(upload_to="hero/", blank=True, null=True, verbose_name="Imagen de Fondo")
    image_url = models.URLField(blank=True, null=True, help_text="URL externa si no se sube imagen local", verbose_name="URL de Imagen de Respaldo")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Slide Hero"
        verbose_name_plural = "Slides Hero"

    def __str__(self):
        return self.title

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or "https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?auto=format&fit=crop&w=1920&q=80"


class Product(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nombre del Producto (ES)")
    name_en = models.CharField(max_length=120, blank=True, verbose_name="Nombre del Producto (EN)")
    scientific_name = models.CharField(max_length=120, blank=True, verbose_name="Nombre Científico")
    variety = models.CharField(max_length=100, default="Hass", verbose_name="Variedad")
    origin = models.CharField(max_length=120, default="Ica / Piura - Perú", verbose_name="Origen / Valle (ES)")
    origin_en = models.CharField(max_length=120, default="Ica / Piura - Peru", verbose_name="Origen / Valle (EN)")
    season = models.CharField(max_length=100, default="Todo el año", verbose_name="Temporada de Cosecha (ES)")
    season_en = models.CharField(max_length=100, default="All year round", verbose_name="Temporada de Cosecha (EN)")
    packing_specs = models.CharField(max_length=160, default="Cajas de 4kg / 10kg en atmósfera controlada", verbose_name="Presentación / Empaque (ES)")
    packing_specs_en = models.CharField(max_length=160, default="4kg / 10kg cartons in controlled atmosphere", verbose_name="Presentación / Empaque (EN)")
    
    # Precios y cotizador
    ref_price_fob_usd = models.DecimalField(max_digits=10, decimal_places=2, default=3.50, verbose_name="Precio Ref. FOB USD")
    price_unit = models.CharField(max_length=50, default="Kg", verbose_name="Unidad de Cotización (Kg / Caja / TM)")
    min_order = models.CharField(max_length=80, default="1 Contenedor Reefer 40ft", verbose_name="Pedido Mínimo")
    min_order_en = models.CharField(max_length=80, default="1 Reefer Container 40ft", verbose_name="Pedido Mínimo (EN)")

    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Foto Principal")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL Imagen Respaldo")
    is_featured = models.BooleanField(default=True, verbose_name="Destacado en Portada")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden de Visualización")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Producto de Exportación"
        verbose_name_plural = "Productos de Exportación"

    def __str__(self):
        return f"{self.name} ({self.variety})"

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?auto=format&fit=crop&w=1200&q=80"


class CompanyStat(models.Model):
    value = models.CharField(max_length=30, verbose_name="Valor (Ej: +25k)")
    label = models.CharField(max_length=100, verbose_name="Etiqueta (ES)")
    label_en = models.CharField(max_length=100, blank=True, verbose_name="Etiqueta (EN)")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        ordering = ['order']
        verbose_name = "Métrica / Cifra"
        verbose_name_plural = "Métricas y Cifras"

    def __str__(self):
        return f"{self.value} - {self.label}"


class Certification(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre Certificación")
    code = models.CharField(max_length=100, blank=True, verbose_name="Alcance / Código (ES)")
    code_en = models.CharField(max_length=100, blank=True, verbose_name="Alcance / Código (EN)")
    image_url = models.URLField(blank=True, null=True, verbose_name="Logo URL")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        ordering = ['order']
        verbose_name = "Certificación de Calidad"
        verbose_name_plural = "Certificaciones"

    def __str__(self):
        return self.name


class QuoteRequest(models.Model):
    CLIENT_TYPE_CHOICES = [
        ('NATURAL_DNI', 'Persona Natural - DNI (Perú)'),
        ('NATURAL_RUC', 'Persona Natural con Negocio - RUC 10 (Perú - Ley RUC)'),
        ('JURIDICA_RUC', 'Persona Jurídica / Empresa - RUC 20 (Perú - Ley RUC)'),
        ('EXTRANJERO', 'Cliente Internacional / Empresa Extranjera (Tax ID / VAT)'),
    ]

    INCOTERM_CHOICES = [
        ('FOB', 'FOB (Free On Board - Puerto Callao / Pisco)'),
        ('CIF', 'CIF (Cost, Insurance & Freight)'),
        ('CFR', 'CFR (Cost & Freight)'),
        ('EXW', 'EXW (Ex Works - Planta Empaque)'),
    ]

    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES, default='JURIDICA_RUC', verbose_name="Tipo de Cliente")
    document_number = models.CharField(max_length=50, verbose_name="N° Documento (DNI / RUC / Tax ID)")
    legal_name = models.CharField(max_length=160, verbose_name="Razón Social / Nombre Completo")
    contact_name = models.CharField(max_length=120, verbose_name="Persona de Contacto")
    country = models.CharField(max_length=100, default="Perú", verbose_name="País")
    email = models.EmailField(verbose_name="Correo Electrónico")
    phone = models.CharField(max_length=50, verbose_name="Teléfono / WhatsApp")
    incoterm = models.CharField(max_length=10, choices=INCOTERM_CHOICES, default='FOB', verbose_name="Incoterm Solicitado")
    destination_port = models.CharField(max_length=120, blank=True, verbose_name="Puerto / Ciudad de Destino")
    notes = models.TextField(blank=True, verbose_name="Notas / Calibres / Requerimientos Específicos")
    
    status = models.CharField(max_length=20, choices=[
        ('NUEVO', 'Nuevo'),
        ('COTIZADO', 'Cotizado'),
        ('EN_NEGOCIACION', 'En Negociación'),
        ('ATENDIDO', 'Atendido'),
    ], default='NUEVO', verbose_name="Estado")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Cotización")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Cotización de Exportación"
        verbose_name_plural = "Cotizaciones de Exportación"

    def clean(self):
        validate_peruvian_document(self.client_type, self.document_number)

    def __str__(self):
        return f"COT-{self.id:04d} | {self.legal_name} ({self.get_client_type_display()}) - {self.country}"


class QuoteItem(models.Model):
    UNIT_CHOICES = [
        ('CONTENEDOR_40', 'Contenedor 40ft High Cube Reefer (~20-22 TM)'),
        ('PALLET', 'Pallets de Exportación'),
        ('CAJAS', 'Cajas Master'),
        ('TONELADAS', 'Toneladas Métricas (TM)'),
    ]

    quote_request = models.ForeignKey(QuoteRequest, related_name="items", on_delete=models.CASCADE, verbose_name="Cotización")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1.00, verbose_name="Cantidad")
    unit = models.CharField(max_length=40, choices=UNIT_CHOICES, default='CONTENEDOR_40', verbose_name="Unidad de Despacho")
    estimated_subtotal_usd = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Subtotal Estimado USD")

    class Meta:
        verbose_name = "Ítem de Cotización"
        verbose_name_plural = "Ítems de Cotización"

    def __str__(self):
        return f"{self.quantity} {self.get_unit_display()} - {self.product.name}"


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="Nombre Completo")
    company = models.CharField(max_length=150, verbose_name="Empresa")
    country = models.CharField(max_length=100, verbose_name="País de Destino")
    email = models.EmailField(verbose_name="Correo Electrónico")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Teléfono / WhatsApp")
    product_interest = models.CharField(max_length=100, blank=True, verbose_name="Producto de Interés")
    message = models.TextField(verbose_name="Requerimiento / Mensaje")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Envío")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"

    def __str__(self):
        return f"{self.full_name} ({self.company}) - {self.country}"
