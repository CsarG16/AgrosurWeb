# Agrosur Perú - Plataforma Web Bilingüe & Cotizador de Agroexportación

Landing page moderna, minimalista y dinámica para **Agrosur**, empresa agroexportadora peruana líder en superfoods y frutas frescas (Palta Hass, Arándanos, Uva de mesa sin semilla, Mango Kent, Espárragos y Jengibre orgánico).

Desarrollada con **Django 6**, base de datos **SQLite**, soporte **bilingüe completo (Español / Inglés)** y un **Cotizador B2B Inteligente** adaptado a la legislación tributaria peruana (Ley del RUC - SUNAT) y a compradores internacionales.

---

## 🌟 Nuevas Funcionalidades Implementadas

### 1. Cotizador Inteligente en SQLite & Frontend
- **Clasificación de Clientes según Normativa Peruana & Global:**
  - 🏢 **Empresa / Persona Jurídica (RUC 20):** Valida RUC de 11 dígitos iniciando con 20 y Razón Social.
  - 💼 **Persona Natural con Negocio (RUC 10):** Valida RUC de 11 dígitos iniciando con 10 (conforme a SUNAT).
  - 👤 **Persona Natural (DNI):** Valida DNI peruano de 8 dígitos numéricos.
  - 🌐 **Cliente Internacional / Extranjero:** Valida Tax ID / VAT Number / EIN y exige el país de destino.
- **Selección Dinámica de Frutos y Volúmenes:**
  - Selección de productos con checkboxes interactivos.
  - Configuración de unidades: *Contenedor 40ft High Cube Reefer (~21 TM)*, *Pallets de Exportación*, *Toneladas Métricas (TM)* o *Cajas Master*.
  - Cálculo instantáneo del estimado FOB en USD según la cotización referencial de mercado.
- **Términos de Despacho & Logística:**
  - Elección de Incoterm: `FOB`, `CIF`, `CFR`, `EXW`.
  - Puerto de destino internacional (Rotterdam, Long Beach, Hamburgo, Shanghai, etc.).
- **Persistencia en SQLite:**
  - Las cotizaciones se guardan en las tablas [`QuoteRequest`](file:///C:/Users/Jualo/Desktop/AGR2/landing/models.py#L98) y [`QuoteItem`](file:///C:/Users/Jualo/Desktop/AGR2/landing/models.py#L137) con código formal correlativo (ej. `COT-0001`).

### 2. Soporte Bilingüe Reactivo (Español / Inglés)
- Selector flotante `[ES] | [EN]` en la barra de navegación que traduce en tiempo real:
  - Textos del Hero, catálogo y fichas de producto.
  - Campos, etiquetas y mensajes de validación del cotizador.
  - Proceso de trazabilidad y certificaciones.
  - Persistencia de la preferencia de idioma en `localStorage`.

---

## 🚀 Inicio Rápido

### 1. Clonar el repositorio y configurar el entorno
```powershell
git clone <URL_DEL_REPOSITORIO>
cd AGR2

# Crear entorno virtual
python -m venv .venv

# Activar en Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias
```powershell
pip install -r requirements.txt
```

### 3. Migraciones y datos iniciales
```powershell
# Aplicar migraciones
python manage.py migrate

# Cargar catálogo de productos y datos de prueba
python manage.py seed_data

# Crear superusuario admin por defecto (admin / admin123)
python manage.py create_admin
```

### 4. Iniciar el servidor
```powershell
python manage.py runserver
```

Abre tu navegador en:
👉 **http://127.0.0.1:8000/**

---

## 🔑 Panel de Administración (Django Admin)
Gestiona frutos, precios referenciales y cotizaciones recibidas en:
👉 **http://127.0.0.1:8000/admin/**

- **Usuario:** `admin`
- **Contraseña:** `admin123`

---

## 🧪 Pruebas Automatizadas
Para verificar que las validaciones tributarias (RUC 20, RUC 10, DNI, Tax ID extranjero) y el sistema bilingüe funcionan a la perfección:
```powershell
python manage.py test
```

---

## 🛠️ Estilos, imágenes e idiomas

### Estilos (Tailwind CLI)
Ya no se usa el CDN de Tailwind. Los estilos se compilan a `static/css/app.css` (se versiona en git, así el servidor no necesita Node):
```powershell
npm install            # solo la primera vez
npm run build:css      # compila (ejecutar antes de subir cambios de plantillas o de main.js)
npm run watch:css      # recompila mientras desarrollas
```
La configuración está en `tailwind.config.js` (colores `agro`/`xpo`, punto de quiebre `nav` = 1200 px para el menú completo).

### Imágenes
Todas las fotos se sirven en WebP. Para añadir o convertir imágenes:
```powershell
python scripts/optimize_images.py --convert foto.png static/images/products/mi-producto.webp
```
Objetivo: 80–150 KB por foto. Las plantillas ya usan `loading="lazy"` en todo lo que está bajo el banner principal.

### Inglés
El español vive en la raíz (`/productos/`) y el inglés bajo `/en/` (`/en/productos/`), con `hreflang`, canonical y sitemap por idioma. El texto del cuerpo en inglés lo traduce `static/js/main.js` (diccionario `translations` y `phraseEN`); el `<title>` y la meta descripción los renderiza Django (bloques `title_en`, `meta_description_en` en cada plantilla).

### Datos de contacto
Teléfono y WhatsApp se leen de variables de entorno y **solo se muestran si existen** (contacto y pie de página):
```
COMPANY_PHONE="+51 1 234 5678"
COMPANY_WHATSAPP="51987654321"
```

### Despliegue en PythonAnywhere
```bash
git pull
pip install -r requirements.txt
python manage.py migrate          # incluye 0007 (slug de productos) y 0008 (imágenes .webp y textos)
python manage.py collectstatic --noinput
# Web > Reload
```

### Cambio al dominio agrosurlatino.com (cuando esté disponible)
Canonical, `og:url`, sitemap y robots usan el dominio de la petición, así que no hay URLs fijas que editar. Falta:
1. Apuntar el dominio a PythonAnywhere (Web > Add a new web app / dominio propio) y activar HTTPS.
2. Variables de entorno: `DJANGO_ALLOWED_HOSTS` (ya incluye `agrosurlatino.com` y `www.`), `DJANGO_CSRF_TRUSTED_ORIGINS="https://agrosurlatino.com,https://www.agrosurlatino.com"` y, si `request.scheme` sale `http`, `DJANGO_BEHIND_PROXY=1`.
3. Redirigir `gablol.pythonanywhere.com` → dominio nuevo y enviar el nuevo `sitemap.xml` a Google Search Console.
