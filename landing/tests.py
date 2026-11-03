from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, HeroSlide, QuoteRequest, QuoteItem


class QuotationAndDecoupledPagesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.hero = HeroSlide.objects.create(
            title="Frutos del Perú",
            title_en="Fruits of Peru",
            tagline="Exportación global",
            tagline_en="Global export",
            order=1,
            is_active=True
        )
        self.product = Product.objects.create(
            name="Palta Hass",
            name_en="Hass Avocado",
            variety="Hass",
            origin="Ica",
            origin_en="Ica Valley",
            season="Marzo a Septiembre",
            season_en="March to September",
            ref_price_fob_usd=3.20,
            order=1
        )

    def test_landing_page_bilingual(self):
        response_es = self.client.get(reverse('landing:index') + '?lang=es')
        self.assertEqual(response_es.status_code, 200)
        self.assertContains(response_es, "AGROSUR")

        response_en = self.client.get(reverse('landing:index') + '?lang=en')
        self.assertEqual(response_en.status_code, 200)

    def test_decoupled_pages_accessible(self):
        # 1. Página de Productos
        res_prod = self.client.get(reverse('landing:productos'))
        self.assertEqual(res_prod.status_code, 200)
        self.assertContains(res_prod, "Palta Hass")

        # 2. Página del Cotizador
        res_coti = self.client.get(reverse('landing:cotizador'))
        self.assertEqual(res_coti.status_code, 200)
        self.assertContains(res_coti, "quote-form")

        # 3. Página de Nosotros / Origen
        res_nos = self.client.get(reverse('landing:nosotros'))
        self.assertEqual(res_nos.status_code, 200)
        self.assertContains(res_nos, "Origen & Campos Propios")

        # 4. Página de Calidad / Certificaciones
        res_cal = self.client.get(reverse('landing:calidad'))
        self.assertEqual(res_cal.status_code, 200)
        self.assertContains(res_cal, "Garantía Sanitaria")

    def test_quote_persona_juridica_and_pdf_generation(self):
        data = {
            'client_type': 'JURIDICA_RUC',
            'document_number': '20609876543',
            'legal_name': 'AGROEXPORT IMPORT SAC',
            'contact_name': 'Carlos Mendoza',
            'country': 'Perú',
            'email': 'carlos@agroexport.pe',
            'phone': '+51 987654321',
            'incoterm': 'FOB',
            'destination_port': 'Callao',
            'items': [
                {'product_id': self.product.id, 'quantity': 2, 'unit': 'CONTENEDOR_40', 'subtotal': 134400}
            ]
        }
        response = self.client.post(
            reverse('landing:submit_quote'),
            data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertIn('COT-', json_data['quote_code'])
        self.assertIn('pdf_url', json_data)

        quote_id = json_data['quote_id']
        pdf_res = self.client.get(reverse('landing:quote_pdf', args=[quote_id]))
        self.assertEqual(pdf_res.status_code, 200)
        self.assertEqual(pdf_res['Content-Type'], 'application/pdf')
        self.assertTrue(pdf_res.content.startswith(b'%PDF-'))

    def test_quote_persona_natural_ruc10_valid(self):
        data = {
            'client_type': 'NATURAL_RUC',
            'document_number': '10456789012',
            'legal_name': 'Mendoza Frutos Frescos',
            'contact_name': 'Carlos Mendoza',
            'country': 'Perú',
            'email': 'cmendoza@frutos.pe',
            'phone': '+51 987654321',
            'incoterm': 'FOB',
            'items': [{'product_id': self.product.id, 'quantity': 1, 'unit': 'PALLET', 'subtotal': 3200}]
        }
        response = self.client.post(
            reverse('landing:submit_quote'),
            data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_quote_cliente_extranjero_valid(self):
        data = {
            'client_type': 'EXTRANJERO',
            'document_number': 'NL-845210987B01',
            'legal_name': 'Rotterdam Fruit B.V.',
            'contact_name': 'Jan Van Dijk',
            'country': 'Países Bajos',
            'email': 'jan@rotterdamfruit.nl',
            'phone': '+31 6 12345678',
            'incoterm': 'CIF',
            'destination_port': 'Port of Rotterdam',
            'items': [{'product_id': self.product.id, 'quantity': 3, 'unit': 'CONTENEDOR_40', 'subtotal': 201600}]
        }
        response = self.client.post(
            reverse('landing:submit_quote'),
            data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_quote_invalid_ruc_rejected(self):
        data = {
            'client_type': 'JURIDICA_RUC',
            'document_number': '10609876543',  # Inválido para Jurídica
            'legal_name': 'TEST EMPRESA',
            'contact_name': 'Test',
            'email': 'test@test.com',
        }
        response = self.client.post(
            reverse('landing:submit_quote'),
            data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()['success'])
