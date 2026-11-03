from django.core.management.base import BaseCommand
from landing.models import HeroSlide, Product, CompanyStat, Certification, QuoteRequest, QuoteItem


class Command(BaseCommand):
    help = "Puebla la base de datos con datos bilingües de Agrosur y productos con cotizador"

    def handle(self, *args, **options):
        self.stdout.write("Actualizando datos bilingües y cotizador de Agrosur...")

        HeroSlide.objects.all().delete()
        Product.objects.all().delete()
        CompanyStat.objects.all().delete()
        Certification.objects.all().delete()

        # Slides bilingües
        HeroSlide.objects.create(
            title="Frutos Selectos de la Tierra Peruana al Mundo",
            title_en="Premium Fruits from the Fertile Lands of Peru to the World",
            tagline="Líderes en agroexportación con los más altos estándares de frescura, empaque y trazabilidad internacional.",
            tagline_en="Agro-export leaders with the highest standards in freshness, automated packaging, and global traceability.",
            badge="Agrosur Perú • Calidad de Exportación",
            badge_en="Agrosur Peru • Export Grade",
            image_url="https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?auto=format&fit=crop&w=1920&q=85",
            order=1,
            is_active=True
        )
        HeroSlide.objects.create(
            title="Sabor, Nutrición y Sustentabilidad Global",
            title_en="Flavor, Superfood Nutrition and Global Sustainability",
            tagline="Cosechados en los valles costeros y andinos con tecnología de riego por goteo y cadena de frío ininterrumpida.",
            tagline_en="Harvested across coastal and highland valleys with computerized drip irrigation and uninterrupted cold chain.",
            badge="Superfoods del Perú",
            badge_en="Peruvian Superfoods",
            image_url="https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1920&q=85",
            order=2,
            is_active=True
        )
        HeroSlide.objects.create(
            title="Conectividad Logística de Primer Nivel",
            title_en="World-Class Maritime & Air Multimodal Logistics",
            tagline="Despachos marítimos y aéreos directos desde el Puerto del Callao y Pisco hacia Norteamérica, Europa y Asia.",
            tagline_en="Direct sea and air dispatches from DP World Callao and Pisco terminals to North America, Europe and Asia.",
            badge="Cadena de Frío Certificada",
            badge_en="Certified Cold Chain",
            image_url="https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1920&q=85",
            order=3,
            is_active=True
        )

        # Productos con campos bilingües y datos de cotización
        products = [
            {
                "name": "Palta Hass",
                "name_en": "Hass Avocado",
                "scientific_name": "Persea americana",
                "variety": "Hass Premium Cat. 1",
                "origin": "Valle de Ica & Chincha",
                "origin_en": "Ica & Chincha Valleys",
                "season": "Marzo a Septiembre",
                "season_en": "March to September",
                "packing_specs": "Cajas de 4.0 kg y 10.0 kg RPC / Calibres 12 al 26",
                "packing_specs_en": "4.0 kg and 10.0 kg cartons / Calibers 12 to 26",
                "ref_price_fob_usd": 3.20,
                "price_unit": "Kg FOB Callao",
                "min_order": "1 Contenedor 40ft (21.5 TM)",
                "min_order_en": "1 40ft Container (21.5 MT)",
                "image_url": "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?auto=format&fit=crop&w=1000&q=80",
                "is_featured": True,
                "order": 1,
            },
            {
                "name": "Arándanos Frescos",
                "name_en": "Fresh Blueberries",
                "scientific_name": "Vaccinium corymbosum",
                "variety": "Ventura, Biloxi & Sekoya",
                "origin": "Olmos & Trujillo",
                "origin_en": "Olmos & Trujillo Valleys",
                "season": "Julio a Febrero",
                "season_en": "July to February",
                "packing_specs": "Clamshells 125g, 310g y 510g en cajas master",
                "packing_specs_en": "Clamshells 125g, 310g & 510g in master cartons",
                "ref_price_fob_usd": 7.80,
                "price_unit": "Kg FOB Callao",
                "min_order": "1 Contenedor 40ft (18 TM) o Carga Aérea",
                "min_order_en": "1 40ft Container (18 MT) or Air Freight",
                "image_url": "https://images.unsplash.com/photo-1498557850523-fd3d118b962e?auto=format&fit=crop&w=1000&q=80",
                "is_featured": True,
                "order": 2,
            },
            {
                "name": "Uva de Mesa Seedless",
                "name_en": "Seedless Table Grapes",
                "scientific_name": "Vitis vinifera",
                "variety": "Autumn Crisp & Sweet Globe",
                "origin": "Valles de Piura e Ica",
                "origin_en": "Piura & Ica Valleys",
                "season": "Octubre a Marzo",
                "season_en": "October to March",
                "packing_specs": "Pouch Bags 4.5 kg / Clamshell 8.2 kg",
                "packing_specs_en": "Pouch Bags 4.5 kg / Clamshell 8.2 kg master",
                "ref_price_fob_usd": 3.60,
                "price_unit": "Kg FOB Pisco/Callao",
                "min_order": "1 Contenedor 40ft (20 TM)",
                "min_order_en": "1 40ft Container (20 MT)",
                "image_url": "https://images.unsplash.com/photo-1596363505729-4190a9506133?auto=format&fit=crop&w=1000&q=80",
                "is_featured": True,
                "order": 3,
            },
            {
                "name": "Mango Kent",
                "name_en": "Kent Mango",
                "scientific_name": "Mangifera indica",
                "variety": "Kent Extra Sweet",
                "origin": "Valle del Alto Piura",
                "origin_en": "Alto Piura Valley",
                "season": "Noviembre a Marzo",
                "season_en": "November to March",
                "packing_specs": "Cajas 4 kg tratamiento hidrotérmico / Aéreo y Marítimo",
                "packing_specs_en": "4 kg cartons hot-water treated / Air & Sea",
                "ref_price_fob_usd": 2.90,
                "price_unit": "Kg FOB Callao",
                "min_order": "1 Contenedor 40ft (21 TM)",
                "min_order_en": "1 40ft Container (21 MT)",
                "image_url": "https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=1000&q=80",
                "is_featured": True,
                "order": 4,
            },
            {
                "name": "Espárrago Verde Fresco",
                "name_en": "Fresh Green Asparagus",
                "scientific_name": "Asparagus officinalis",
                "variety": "UC 157 F1",
                "origin": "Ica & La Libertad",
                "origin_en": "Ica & La Libertad",
                "season": "Todo el año (Pico Ago-Dic)",
                "season_en": "Year-round (Peak Aug-Dec)",
                "packing_specs": "Atados piramidales de 5 kg / 11 lb máster refrigerado",
                "packing_specs_en": "Pyramid bunches 5 kg / 11 lb master box",
                "ref_price_fob_usd": 4.10,
                "price_unit": "Kg FOB Callao",
                "min_order": "Pallets Aéreos o Contenedor Marítimo",
                "min_order_en": "Air Pallets or Sea Container",
                "image_url": "https://images.unsplash.com/photo-1515471204630-e60780ebd1ee?auto=format&fit=crop&w=1000&q=80",
                "is_featured": True,
                "order": 5,
            },
            {
                "name": "Jengibre & Cúrcuma Orgánica",
                "name_en": "Organic Ginger & Turmeric",
                "scientific_name": "Zingiber officinale",
                "variety": "Criollo Orgánico Certificado",
                "origin": "Selva Central (Satipo - Junín)",
                "origin_en": "Central Rainforest (Junín)",
                "season": "Junio a Febrero",
                "season_en": "June to February",
                "packing_specs": "Cajas de cartón corrugado 13.6 kg (30 lb)",
                "packing_specs_en": "13.6 kg (30 lb) corrugated export cartons",
                "ref_price_fob_usd": 2.70,
                "price_unit": "Kg FOB Callao",
                "min_order": "1 Contenedor 40ft (21 TM)",
                "min_order_en": "1 40ft Container (21 MT)",
                "image_url": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=1000&q=80",
                "is_featured": True,
                "order": 6,
            },
        ]
        for p in products:
            Product.objects.create(**p)

        stats = [
            {"value": "+35,000", "label": "Toneladas métricas exportadas anualmente", "label_en": "Metric tons exported yearly to global markets", "order": 1},
            {"value": "32+", "label": "Países y puertos de destino en 4 continentes", "label_en": "Destination countries & ports on 4 continents", "order": 2},
            {"value": "100%", "label": "Trazabilidad digital desde el campo de cultivo", "label_en": "Digital farm-to-shelf batch traceability", "order": 3},
            {"value": "2,400 Ha", "label": "Áreas productivas bajo riego tecnificado", "label_en": "Hectares under precision drip irrigation", "order": 4},
        ]
        for s in stats:
            CompanyStat.objects.create(**s)

        certs = [
            {"name": "GLOBAL G.A.P.", "code": "Buenas Prácticas Agrícolas Internacionales", "code_en": "Good Agricultural Practices Worldwide", "order": 1},
            {"name": "SMETA / SEDEX", "code": "Auditoría Ética y Responsabilidad Social", "code_en": "Ethical Trade & Labor Responsibility", "order": 2},
            {"name": "BRCGS Food Safety", "code": "Inocuidad y Estándar de Empaque Grado A", "code_en": "Global Food Safety & Packing Grade A", "order": 3},
            {"name": "USDA ORGANIC", "code": "Certificación para el mercado norteamericano", "code_en": "Certified Organic for US & Canada Markets", "order": 4},
            {"name": "SENASA PERÚ", "code": "Certificación Fitosanitaria Oficial de Origen", "code_en": "Official Peruvian Phytosanitary Guarantee", "order": 5},
        ]
        for c in certs:
            Certification.objects.create(**c)

        # Crear una cotización de muestra para que se visualice en el Admin
        sample_quote = QuoteRequest.objects.create(
            client_type='JURIDICA_RUC',
            document_number='20601234567',
            legal_name='AGROEXPORTADORA DEL PACIFICO S.A.C.',
            contact_name='Gonzalo Valdivia',
            country='Perú',
            email='comercial@agropacifico.pe',
            phone='+51 987 654 321',
            incoterm='FOB',
            destination_port='DP World Callao',
            notes='Requerimos 2 contenedores de Palta Hass calibre 16-18 para despacho semana 24.'
        )
        palta = Product.objects.filter(name__icontains="Palta").first()
        if palta:
            QuoteItem.objects.create(
                quote_request=sample_quote,
                product=palta,
                quantity=2,
                unit='CONTENEDOR_40',
                estimated_subtotal_usd=137600.00
            )

        self.stdout.write(self.style.SUCCESS("¡Base de datos SQLite actualizada con éxito con datos bilingües y cotizador!"))
