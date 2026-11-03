from django.contrib import admin
from django.utils.html import format_html
from .models import (
    HeroSlide,
    ProductCategory,
    Product,
    CompanyStat,
    Certification,
    QuoteRequest,
    QuoteItem,
    ContactMessage,
)

admin.site.site_header = "Agro Sur Latino S.A.C. — Panel de Administración"
admin.site.site_title = "Admin Agro Sur Latino"
admin.site.index_title = "Gestión de Catálogo SQLite3 (Granos Andinos, Semillas, Menestras y Cotizaciones)"


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'badge', 'order', 'is_active')
    list_display_links = ('image_preview', 'title')
    list_editable = ('badge', 'order', 'is_active')

    def image_preview(self, obj):
        return format_html(
            '<img src="{}" style="width: 56px; height: 70px; object-fit: cover; border-radius: 6px; border: 1px solid #ddd;" />',
            obj.get_image
        )
    image_preview.short_description = "Vista Previa"


class ProductInline(admin.TabularInline):
    model = Product
    fields = ('name', 'modality', 'variety', 'ref_price_fob_usd', 'is_featured', 'is_active', 'order')
    extra = 0


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'name_en', 'slug', 'watermark_text', 'order', 'is_active')
    list_display_links = ('image_preview', 'name')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductInline]

    def image_preview(self, obj):
        return format_html(
            '<img src="{}" style="width: 52px; height: 64px; object-fit: cover; border-radius: 6px; border: 1px solid #ddd;" />',
            obj.get_image
        )
    image_preview.short_description = "Foto Panel"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'image_preview',
        'name',
        'category',
        'modality',
        'origin',
        'ref_price_fob_usd',
        'is_featured',
        'is_active',
        'order',
    )
    list_display_links = ('image_preview', 'name')
    list_editable = (
        'category',
        'modality',
        'ref_price_fob_usd',
        'is_featured',
        'is_active',
        'order',
    )
    list_filter = ('category', 'modality', 'is_featured', 'is_active')
    search_fields = ('name', 'name_en', 'scientific_name', 'variety', 'origin')
    fieldsets = (
        ("Identificación y Categoría", {
            'fields': ('category', 'name', 'name_en', 'scientific_name', 'modality', 'variety')
        }),
        ("Fotografía Visual (Subir Archivo o Pegar URL)", {
            'fields': ('image', 'image_url')
        }),
        ("Origen, Stock y Empaque de Exportación", {
            'fields': ('origin', 'origin_en', 'season', 'season_en', 'packing_specs', 'packing_specs_en')
        }),
        ("Precios FOB y Visualización en Web", {
            'fields': ('ref_price_fob_usd', 'price_unit', 'min_order', 'min_order_en', 'is_featured', 'is_active', 'order')
        }),
    )

    def image_preview(self, obj):
        return format_html(
            '<img src="{}" style="width: 54px; height: 54px; object-fit: cover; border-radius: 8px; border: 1px solid #d6d3d1;" />',
            obj.get_image
        )
    image_preview.short_description = "Foto"


@admin.register(CompanyStat)
class CompanyStatAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'label_en', 'order')
    list_editable = ('order',)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('logo_preview', 'name', 'code', 'code_en', 'order')
    list_display_links = ('logo_preview', 'name')
    list_editable = ('code', 'order')

    def logo_preview(self, obj):
        return format_html(
            '<img src="{}" style="height: 44px; width: auto; max-width: 90px; object-fit: contain; background: #fff; padding: 4px; border-radius: 6px; border: 1px solid #ddd;" />',
            obj.get_image
        )
    logo_preview.short_description = "Logo"


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 1


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'legal_name', 'client_type', 'document_number', 'country', 'incoterm', 'status', 'created_at')
    list_filter = ('client_type', 'incoterm', 'status', 'created_at')
    list_editable = ('status',)
    search_fields = ('legal_name', 'document_number', 'contact_name', 'email', 'destination_port')
    inlines = [QuoteItemInline]
    readonly_fields = ('created_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company', 'country', 'email', 'product_interest', 'created_at')
    search_fields = ('full_name', 'company', 'country', 'email')
    readonly_fields = ('created_at',)
