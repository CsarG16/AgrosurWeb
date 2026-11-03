from django.test import TestCase, Client
from django.urls import reverse
from .models import ProductCategory, Product, HeroSlide, QuoteRequest, QuoteItem, ContactMessage


class QuotationAndDecoupledPagesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.hero = HeroSlide.objects.create(
            title="Granos y semillas andinas",
            title_en="Andean grains and seeds",
            tagline="Granos Andinos",
            tagline_en="Andean Grains",
            order=1,
            is_active=True
        )
        self.category = ProductCategory.objects.create(
            name="Granos y Semillas Andinas",
            name_en="Andean Grains & Seeds",
            slug="granos-andinos",
            order=1,
            is_active=True
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Quinua Blanca en Grano",
            name_en="White Quinoa Grain",
            modality="ORGANICO_CONVENCIONAL",
            variety="Pureza 99.95%",
            origin="Ayacucho / Puno",
            origin_en="Ayacucho / Puno",
            season="Todo el año",
            season_en="All year round",
            ref_price_fob_usd=2.85,
            order=1,
            is_active=True,
            is_featured=True
        )

    def test_landing_page_bilingual_and_visual_catalog(self):
        response_es = self.client.get(reverse('landing:index') + '?lang=es')
        self.assertEqual(response_es.status_code, 200)
        self.assertContains(response_es, "AGRO SUR LATINO")
        self.assertContains(response_es, "Quinua Blanca en Grano")
        self.assertContains(response_es, "Granos y semillas andinas")

        response_en = self.client.get(reverse('landing:index') + '?lang=en')
        self.assertEqual(response_en.status_code, 200)

    def test_decoupled_pages_accessible(self):
        # 1. Página Visual de Productos desde SQLite3
        res_prod = self.client.get(reverse('landing:productos'))
        self.assertEqual(res_prod.status_code, 200)
        self.assertContains(res_prod, "Quinua Blanca en Grano")
        self.assertContains(res_prod, "Granos y Semillas Andinas")

        # 2. Página del Cotizador B2B
        res_coti = self.client.get(reverse('landing:cotizador'))
        self.assertEqual(res_coti.status_code, 200)
        self.assertContains(res_coti, "quote-form")

        # 3. Página de Sobre Nosotros (About Us)
        res_nos = self.client.get(reverse('landing:nosotros'))
        self.assertEqual(res_nos.status_code, 200)
        self.assertContains(res_nos, "AGRO SUR LATINO S.A.C.")
        self.assertContains(res_nos, "20517805662")

        # 4. Página de Calidad / Certificaciones
        res_cal = self.client.get(reverse('landing:calidad'))
        self.assertEqual(res_cal.status_code, 200)
        self.assertContains(res_cal, "Garantía Sanitaria")

    def test_quote_persona_juridica_and_pdf_generation(self):
        data = {
            'client_type': 'JURIDICA_RUC',
            'document_number': '20517805662',
            'legal_name': 'AGRO SUR LATINO IMPORT SAC',
            'contact_name': 'David Comercial',
            'country': 'Perú',
            'email': 'david@agrosurlatino.com',
            'phone': '+51 987654321',
            'incoterm': 'FOB',
            'destination_port': 'Callao',
            'items': [
                {'product_id': self.product.id, 'quantity': 1, 'unit': 'CONTENEDOR_40', 'subtotal': 57000}
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
            'legal_name': 'Mendoza Granos Andinos',
            'contact_name': 'Carlos Mendoza',
            'country': 'Perú',
            'email': 'cmendoza@granos.pe',
            'phone': '+51 987654321',
            'incoterm': 'FOB',
            'items': [{'product_id': self.product.id, 'quantity': 1, 'unit': 'PALLET', 'subtotal': 2850}]
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
            'legal_name': 'Rotterdam Grains B.V.',
            'contact_name': 'Jan Van Dijk',
            'country': 'Países Bajos',
            'email': 'jan@rotterdamgrains.nl',
            'phone': '+31 6 12345678',
            'incoterm': 'CIF',
            'destination_port': 'Port of Rotterdam',
            'items': [{'product_id': self.product.id, 'quantity': 2, 'unit': 'CONTENEDOR_40', 'subtotal': 114000}]
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
            'document_number': '10609876543',
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

    def test_contact_message_submission(self):
        response = self.client.post(
            reverse('landing:submit_contact'),
            {
                'full_name': 'Ana Torres',
                'company': 'Andes Organic Foods',
                'country': 'Estados Unidos',
                'email': 'ana@andesorganic.com',
                'product_interest': 'Quinua Blanca en Grano',
                'message': 'Interesados en 2 contenedores de Quinua Blanca Orgánica.'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertEqual(ContactMessage.objects.count(), 1)
