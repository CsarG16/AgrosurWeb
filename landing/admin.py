from django.contrib import admin
from .models import HeroSlide, Product, CompanyStat, Certification, QuoteRequest, QuoteItem, ContactMessage


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_en', 'badge', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'variety', 'origin', 'ref_price_fob_usd', 'price_unit', 'is_featured', 'order')
    list_editable = ('is_featured', 'order')
    search_fields = ('name', 'name_en', 'variety', 'origin')


@admin.register(CompanyStat)
class CompanyStatAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'label_en', 'order')
    list_editable = ('order',)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'order')
    list_editable = ('order',)


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 1


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'legal_name', 'client_type', 'document_number', 'country', 'incoterm', 'status', 'created_at')
    list_filter = ('client_type', 'incoterm', 'status', 'created_at')
    search_fields = ('legal_name', 'document_number', 'contact_name', 'email', 'destination_port')
    inlines = [QuoteItemInline]
    readonly_fields = ('created_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company', 'country', 'email', 'product_interest', 'created_at')
    search_fields = ('full_name', 'company', 'country', 'email')
    readonly_fields = ('created_at',)
