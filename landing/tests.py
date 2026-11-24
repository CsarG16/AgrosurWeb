from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse
from django.test import override_settings
from .models import ProductCategory, Product, HeroSlide, QuoteRequest, QuoteItem, ContactMessage, Certification


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
        response_es = self.client.get(reverse('landing:index'))
        self.assertEqual(response_es.status_code, 200)
        self.assertContains(response_es, "AGRO SUR LATINO")
        self.assertContains(response_es, "Quinua Blanca en Grano")
        self.assertRegex(response_es.content.decode(), r'<h1[^>]*>\s*Un futuro sembrado hace miles de años')
        self.assertContains(response_es, "Mejora continua. Stock todo el año.")
        self.assertContains(response_es, "Certificaciones")

        response_en = self.client.get('/en/')
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
        self.assertNotContains(res_nos, "20517805662")  # el RUC de la empresa no se publica en la web

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


class FeedbackRoundTests(TestCase):
    """Cubre los puntos del feedback v1: inglés /en/ con hreflang, slug de producto, certificaciones, contacto."""

    def setUp(self):
        cache.clear()
        self.category = ProductCategory.objects.create(name="Legumbres", slug="legumbres", order=1)
        self.habas = Product.objects.create(category=self.category, name="Habas Secas", name_en="Dry Fava Beans", order=1)
        self.pallar = Product.objects.create(category=self.category, name="Pallar Bebé y Pallares", name_en="Baby Lima Beans & Giant Pallar", order=2)
        for i, name in enumerate(['HACCP', 'MAYA', 'ÖKO-GARANTIE'], start=1):
            Certification.objects.create(name=name, order=i)

    def test_slug_se_genera_y_es_unico(self):
        self.assertEqual(self.habas.slug, 'habas-secas')
        copia = Product.objects.create(name="Habas Secas")
        self.assertEqual(copia.slug, 'habas-secas-2')

    def test_ingles_en_url_propia_con_hreflang_y_canonical(self):
        for path, es_path in [('/en/', '/'), ('/en/productos/', '/productos/'), ('/en/calidad/', '/calidad/')]:
            html = self.client.get(path).content.decode()
            self.assertIn('<html lang="en"', html)
            self.assertIn('hreflang="en" href="http://testserver' + path + '"', html)
            self.assertIn('hreflang="es" href="http://testserver' + es_path + '"', html)
            self.assertIn('rel="canonical" href="http://testserver' + path + '"', html)
        self.assertIn('<title>Product Catalog', self.client.get('/en/productos/').content.decode())
        # el español sigue en la raíz y enlaza a su versión en inglés
        es = self.client.get('/productos/').content.decode()
        self.assertIn('<html lang="es"', es)
        self.assertIn('href="/en/productos/"', es)
        self.assertIn('<title>Catálogo Visual', es)

    def test_enlaces_internos_en_ingles_conservan_el_prefijo(self):
        html = self.client.get('/en/').content.decode()
        self.assertIn('href="/en/productos/"', html)
        self.assertIn('data-quote-url="/en/cotizador/"', html)

    def test_sitemap_incluye_ambos_idiomas(self):
        xml = self.client.get('/sitemap.xml').content.decode()
        self.assertIn('<loc>http://testserver/en/productos/</loc>', xml)
        self.assertIn('hreflang="en"', xml)
        self.assertIn('Disallow: /en/api/', self.client.get('/robots.txt').content.decode())

    def test_cotizador_preselecciona_producto_por_slug(self):
        html = self.client.get(reverse('landing:cotizador') + '?producto=pallar-bebe-y-pallares').content.decode()
        checked = [line for line in html.splitlines() if 'quote-prod-checkbox' in line and ' checked ' in line]
        self.assertEqual(len(checked), 1)
        self.assertIn('Pallar Bebé y Pallares', checked[0])
        # slug inexistente: no marca nada desde el servidor (el JS marca el primero)
        html = self.client.get(reverse('landing:cotizador') + '?producto=no-existe').content.decode()
        self.assertFalse([l for l in html.splitlines() if 'quote-prod-checkbox' in l and ' checked ' in l])

    def test_modal_y_tarjetas_accesibles(self):
        html = self.client.get(reverse('landing:productos')).content.decode()
        self.assertIn('"slug": "habas-secas"', html)
        self.assertIn('role="button" tabindex="0"', html)
        self.assertIn('data-quote-url="/cotizador/"', html)
        self.assertNotIn('src="" alt="Producto"', html)

    def test_certificaciones_unificadas_desde_la_base_de_datos(self):
        footer = self.client.get(reverse('landing:index')).content.decode()
        self.assertIn('HACCP • MAYA • ÖKO-GARANTIE', footer)
        calidad = self.client.get(reverse('landing:calidad')).content.decode()
        self.assertIn('Agro Sur Latino S.A.C.: HACCP, MAYA, ÖKO-GARANTIE.', calidad)

    def test_titulo_nosotros_sin_mezcla_de_idiomas(self):
        self.assertIn('<title>Sobre Nosotros | Agro Sur Latino S.A.C.</title>', self.client.get(reverse('landing:nosotros')).content.decode())
        self.assertIn('<title>About Us | Agro Sur Latino S.A.C.</title>', self.client.get('/en/nosotros/').content.decode())

    def test_direccion_completa_y_telefono_solo_si_esta_configurado(self):
        html = self.client.get(reverse('landing:index')).content.decode()
        self.assertEqual(html.count('Jr. Antonio José de Sucre Mz. I Lte. 11'), 2)  # contacto + pie
        self.assertIn('google.com.pe/maps/place/AGROSUR+LATINO', html)
        self.assertNotIn('wa.me', html)
        with override_settings(COMPANY_WHATSAPP='+51 987 654 321', COMPANY_PHONE='+51 1 234 5678'):
            html = self.client.get(reverse('landing:index')).content.decode()
            self.assertIn('https://wa.me/51987654321?text=', html)
            self.assertIn('href="tel:+5112345678"', html)

    def test_pallar_en_espanol_usa_y(self):
        html = self.client.get(reverse('landing:productos')).content.decode()
        self.assertIn('Pallar Bebé y Pallares', html)
        self.assertNotIn('Pallar Bebé &amp; Pallares', html)


class FinalChangesTests(TestCase):
    """Cambios finales: lema, página Social, cotización Perú sin Incoterm, productos en inglés, años de trayectoria."""

    def setUp(self):
        cache.clear()
        self.product = Product.objects.create(name="Quinua Blanca en Grano", name_en="White Quinoa Grain", ref_price_fob_usd=2.85, order=1)

    def post_quote(self, **extra):
        data = {
            'client_type': 'JURIDICA_RUC', 'document_number': '20517805662', 'legal_name': 'ACME SAC',
            'contact_name': 'Ana', 'country': 'Perú', 'email': 'ana@example.com', 'phone': '999',
            'incoterm': 'CIF', 'destination_port': 'Rotterdam', 'lang': 'es',
            'items': [{'product_id': self.product.id, 'quantity': 1, 'unit': 'SACOS_25KG'}],
        }
        data.update(extra)
        r = self.client.post(reverse('landing:submit_quote'), data, content_type='application/json')
        self.assertEqual(r.status_code, 200, r.content)
        return QuoteRequest.objects.get(pk=r.json()['quote_id']), r.json()

    def test_lema_nuevo_en_web_y_sin_el_anterior(self):
        for path in ['/', '/nosotros/']:
            html = self.client.get(path).content.decode()
            self.assertIn('Un futuro sembrado hace miles de años', html)
            self.assertNotIn('De los productores hacia el mundo', html)
        self.assertIn('A future sown thousands of years ago', self.client.get('/en/nosotros/').content.decode())

    def test_pagina_social_en_menu_y_sitemap(self):
        res = self.client.get('/social/')
        self.assertContains(res, 'Fortalecimiento de las capacidades humanas')
        for district in ['Quinua', 'Acocro', 'Tambillo', 'Acos Vinchos', 'Morochucos']:
            self.assertContains(res, district)
        self.assertEqual(res.content.decode().count('images/social/etapa-'), 10)
        self.assertContains(self.client.get('/en/social/'), '<html lang="en"')
        self.assertContains(self.client.get('/'), 'href="/social/"')
        self.assertContains(self.client.get('/sitemap.xml'), '/social/')

    def test_cotizacion_peru_sin_incoterm_ni_puerto(self):
        for client_type, doc in [('JURIDICA_RUC', '20517805662'), ('NATURAL_RUC', '10456789012'), ('NATURAL_DNI', '45678901')]:
            quote, _ = self.post_quote(client_type=client_type, document_number=doc)
            self.assertEqual(quote.incoterm, '')
            self.assertEqual(quote.destination_port, '')
            self.assertEqual(quote.currency, 'PEN')
        export, _ = self.post_quote(client_type='EXTRANJERO', document_number='NL-845210987B01', country='Países Bajos')
        self.assertEqual((export.incoterm, export.destination_port), ('CIF', 'Rotterdam'))

    def test_pdf_se_genera_para_peru_exportacion_e_ingles(self):
        from .pdf import generate_quotation_pdf
        peru_es, _ = self.post_quote()
        peru_en, _ = self.post_quote(lang='en')
        export_en, _ = self.post_quote(client_type='EXTRANJERO', document_number='NL-845210987B01', country='Países Bajos', lang='en')
        self.assertEqual(peru_en.lang, 'en')
        for quote in (peru_es, peru_en, export_en):
            self.assertTrue(generate_quotation_pdf(quote).startswith(b'%PDF'))

    def test_resumen_en_ingles_usa_nombre_y_cantidad_en_ingles(self):
        def estimate(lang, qty):
            return self.client.post(reverse('landing:quote_estimate'), {
                'client_type': 'EXTRANJERO', 'lang': lang,
                'items': [{'product_id': self.product.id, 'quantity': qty, 'unit': 'SACOS_25KG'}]}, content_type='application/json').json()['items'][0]
        en = estimate('en', 1)
        self.assertEqual((en['name'], en['label']), ('White Quinoa Grain', '1 × 25 kg bag'))
        self.assertEqual(estimate('en', 3)['label'], '3 × 25 kg bags')
        es = estimate('es', 2)
        self.assertEqual((es['name'], es['label']), ('Quinua Blanca en Grano', '2 × sacos de 25 kg'))

    def test_anios_de_trayectoria_calculados_desde_la_fundacion(self):
        from django.utils import timezone
        from .models import CompanyStat
        CompanyStat.objects.create(value='2007', label='Año de fundación', label_en='Year founded', order=1)
        years = timezone.localdate().year - 2007
        html = self.client.get('/nosotros/').content.decode()
        self.assertIn(f'{years} años de trayectoria', html)
        self.assertNotIn('+17', html)
        # el cálculo sigue a settings.COMPANY_FOUNDED_YEAR (la cifra mostrada es la de la fila cuyo valor es ese año)
        CompanyStat.objects.all().update(value='2000')
        with override_settings(COMPANY_FOUNDED_YEAR=2000):
            self.assertIn(f'{timezone.localdate().year - 2000} años de trayectoria', self.client.get('/nosotros/').content.decode())


class EnglishServerHtmlTests(TestCase):
    """v3: las páginas /en/ llegan del servidor ya en inglés (no solo traducidas por JavaScript)."""

    def setUp(self):
        cache.clear()
        cat = ProductCategory.objects.create(name="Granos y Semillas Andinas", name_en="Andean Grains & Seeds", slug="granos", order=1)
        Product.objects.create(category=cat, name="Habas Secas", name_en="Dry Fava Beans", order=1)

    def test_h1_y_textos_en_ingles_desde_el_servidor(self):
        cases = {
            '/en/': 'A future sown thousands of years ago',
            '/en/nosotros/': 'Peruvian Andean grains, export quality',
            '/en/productos/': 'Our Products',
            '/en/calidad/': 'Food Safety &amp; Global Certifications',
            '/en/cotizador/': 'Request a quote online',
            '/en/social/': 'Strengthening human capabilities',
        }
        for path, h1 in cases.items():
            html = self.client.get(path).content.decode()
            self.assertRegex(html, r'<h1[^>]*>\s*' + h1)
        # la versión en español: el título de portada pasó a Sobre Nosotros
        self.assertRegex(self.client.get('/nosotros/').content.decode(), r'<h1[^>]*>\s*Granos andinos del Perú, con calidad de exportación')

    def test_formulario_de_contacto_en_ingles(self):
        html = self.client.get('/en/').content.decode()
        for text in ['placeholder="Company *"', 'placeholder="Email *"', 'placeholder="Volume or requirements..."', 'placeholder="Name *"']:
            self.assertIn(text, html)
        self.assertNotIn('placeholder="Empresa *"', html)

    def test_nombres_y_etiquetas_de_productos_en_ingles(self):
        html = self.client.get('/en/productos/').content.decode()
        self.assertIn('aria-label="View details of Dry Fava Beans"', html)
        self.assertIn('alt="Dry Fava Beans"', html)
        self.assertRegex(html, r'data-en="Dry Fava Beans">\s*Dry Fava Beans')
        self.assertIn('aria-label="Andean Grains &amp; Seeds"', html)
        # el diccionario para main.js no se traduce (sigue llevando las claves en español)
        self.assertIn('id="i18n-data"', html)
        self.assertIn('"Calidad:": "Quality:"', html.replace('\u00e9', 'é'))

    def test_imagen_del_modal_con_src_de_respaldo(self):
        html = self.client.get('/productos/').content.decode()
        self.assertIn('id="modal-image" src="data:image/gif;base64,', html)
        self.assertNotIn('src=""', html)
