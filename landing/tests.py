from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse
from .models import ProductCategory, Product, HeroSlide, QuoteRequest, QuoteItem, ContactMessage


class QuotationAndDecoupledPagesTests(TestCase):
    def setUp(self):
        cache.clear()
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
        self.assertContains(response_es, "Granos andinos del Perú, con calidad de exportación")
        self.assertContains(response_es, "Mejora continua. Stock todo el año.")
        self.assertContains(response_es, "Certificaciones")

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
                {'product_id': self.product.id, 'quantity': 4, 'unit': 'SACOS_25KG', 'subtotal': 1}
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

        quote = QuoteRequest.objects.get(id=json_data['quote_id'])
        pdf_res = self.client.get(json_data['pdf_url'])
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
            'items': [{'product_id': self.product.id, 'quantity': 10, 'unit': 'KILOS'}]
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
            'items': [{'product_id': self.product.id, 'quantity': 2, 'unit': 'CONTENEDOR_FCL'}]
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


class QuoteSecurityAndPricingTests(TestCase):
    """Casos del informe QA (COT-0002 a COT-0008)."""

    def setUp(self):
        cache.clear()
        self.product = Product.objects.create(name="Quinua Blanca", ref_price_fob_usd=2.85)
        self.url = reverse('landing:submit_quote')

    def payload(self, items, **extra):
        data = {
            'client_type': 'EXTRANJERO', 'document_number': 'NL-845210987B01',
            'legal_name': 'Rotterdam Grains B.V.', 'contact_name': 'Jan', 'country': 'Países Bajos',
            'email': 'jan@example.com', 'phone': '+31 6 1234', 'incoterm': 'FOB', 'items': items,
        }
        data.update(extra)
        return data

    def post(self, data):
        return self.client.post(self.url, data, content_type='application/json')

    def test_total_calculado_en_servidor_ignora_subtotal_del_navegador(self):
        r = self.post(self.payload([{'product_id': self.product.id, 'quantity': 1, 'unit': 'CONTENEDOR_FCL', 'subtotal': 1}]))
        self.assertEqual(r.status_code, 200)
        item = QuoteItem.objects.get()
        self.assertEqual(str(item.estimated_subtotal_usd), '57000.00')  # 20 000 kg x 2.85

    def test_precio_con_coma_decimal_no_se_trunca(self):
        r = self.post(self.payload([{'product_id': self.product.id, 'quantity': '2,5', 'unit': 'TONELADAS'}]))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(QuoteItem.objects.get().estimated_subtotal_usd), '7125.00')  # 2.5 TM x 1000 x 2.85

    def test_datos_imposibles_son_rechazados_sin_crear_registros(self):
        bad = [
            [{'product_id': self.product.id, 'quantity': -5, 'unit': 'TONELADAS'}],
            [{'product_id': self.product.id, 'quantity': 0, 'unit': 'TONELADAS'}],
            [{'product_id': self.product.id, 'quantity': 1e12, 'unit': 'CONTENEDOR_FCL'}],
            [{'product_id': 99999, 'quantity': 1, 'unit': 'CONTENEDOR_FCL'}],
            [{'product_id': self.product.id, 'quantity': 1, 'unit': 'INVENTADA'}],
            [],
        ]
        for items in bad:
            cache.clear()
            r = self.post(self.payload(items))
            self.assertEqual(r.status_code, 400, items)
        self.assertEqual(QuoteRequest.objects.count(), 0)
        self.assertEqual(QuoteItem.objects.count(), 0)

    def test_cliente_peru_cotiza_en_soles_con_igv(self):
        data = self.payload(
            [{'product_id': self.product.id, 'quantity': 10, 'unit': 'KILOS'}],
            client_type='JURIDICA_RUC', document_number='20517805662', country='Perú',
        )
        self.assertEqual(self.post(data).status_code, 200)
        q = QuoteRequest.objects.get()
        self.assertEqual(q.currency, 'PEN')
        # 2.85 x 3.75 x 1.18 = 12.61 por kg (redondeado) -> 10 kg = 126.10
        self.assertEqual(str(QuoteItem.objects.get().estimated_subtotal_usd), '126.10')

    def test_peru_no_acepta_contenedores(self):
        data = self.payload(
            [{'product_id': self.product.id, 'quantity': 1, 'unit': 'CONTENEDOR_FCL'}],
            client_type='NATURAL_DNI', document_number='12345678',
        )
        self.assertEqual(self.post(data).status_code, 400)

    def test_pdf_solo_con_token_aleatorio(self):
        self.post(self.payload([{'product_id': self.product.id, 'quantity': 1, 'unit': 'CONTENEDOR_FCL'}]))
        q = QuoteRequest.objects.get()
        self.assertEqual(self.client.get(f'/cotizacion/{q.id}/pdf/').status_code, 404)
        ok = self.client.get(reverse('landing:quote_pdf', args=[q.public_token]))
        self.assertEqual(ok.status_code, 200)
        self.assertTrue(ok.content.startswith(b'%PDF-'))

    def test_limite_de_envios_por_ip(self):
        statuses = [
            self.post(self.payload([{'product_id': self.product.id, 'quantity': 1, 'unit': 'PALLET'}], email=f'a{i}@example.com')).status_code
            for i in range(7)
        ]
        self.assertEqual(statuses[:5], [200] * 5)
        self.assertEqual(statuses[5:], [429, 429])

    def test_honeypot_no_crea_cotizacion(self):
        r = self.post(self.payload([{'product_id': self.product.id, 'quantity': 1, 'unit': 'PALLET'}], website='http://spam'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(QuoteRequest.objects.count(), 0)

    def test_estimate_endpoint_y_precio_no_publicado_en_html(self):
        r = self.client.post(reverse('landing:quote_estimate'), {
            'client_type': 'EXTRANJERO', 'items': [{'product_id': self.product.id, 'quantity': 1, 'unit': 'CONTENEDOR_FCL'}]},
            content_type='application/json')
        self.assertEqual(r.json()['total'], 'US$ 57,000.00')
        for name in ['landing:index', 'landing:productos']:
            html = self.client.get(reverse(name)).content.decode()
            self.assertNotIn('2,85', html)
            self.assertNotIn('2.85', html)
        # el cotizador sí muestra el precio por kg, con punto decimal
        coti = self.client.get(reverse('landing:cotizador')).content.decode()
        self.assertIn('data-usd="US$ 2.85"', coti)
        self.assertNotIn('2,85', coti)

    def test_robots_sitemap_y_footer_sin_admin(self):
        self.assertContains(self.client.get('/robots.txt'), 'Sitemap:')
        self.assertContains(self.client.get('/sitemap.xml'), '/productos/')
        self.assertNotContains(self.client.get(reverse('landing:index')), 'Admin SQLite3')
