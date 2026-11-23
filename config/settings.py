from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import os

# En producción definir DJANGO_SECRET_KEY y (opcional) DJANGO_ALLOWED_HOSTS en el entorno.
# DEBUG queda apagado en producción (WSGI). En local se enciende solo con `runserver`,
# o forzándolo con DJANGO_DEBUG=1 / apagándolo con DJANGO_DEBUG=0.
import sys
DEBUG = os.environ.get('DJANGO_DEBUG', '1' if 'runserver' in sys.argv else '0') == '1'
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-e%i$7)r5y!p!_2b8%k-l!nu*v@^p%x8+!o3=)8lhi$89g06s0*',
)
ALLOWED_HOSTS = os.environ.get(
    'DJANGO_ALLOWED_HOSTS',
    'gablol.pythonanywhere.com,agrosurlatino.com,www.agrosurlatino.com,localhost,127.0.0.1,testserver',
).split(',')
# Orígenes https de confianza para formularios (ej. 'https://agrosurlatino.com,https://www.agrosurlatino.com')
CSRF_TRUSTED_ORIGINS = [o for o in os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',') if o]
# Detrás del proxy de PythonAnywhere: que request.scheme sea https (canonical, og:url, sitemap)
if os.environ.get('DJANGO_BEHIND_PROXY') == '1':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# YouTube exige el referrer del sitio (Django envía 'same-origin' por defecto => Error 153)
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Datos de empresa: una sola fuente para web y PDF
COMPANY_ADDRESS = 'Jr. Antonio José de Sucre Mz. I Lte. 11, Asoc. Viv. Huertos de Huachipa – Lurigancho'
COMPANY_EMAIL = 'david@agrosurlatino.com'
COMPANY_FOUNDED_YEAR = 2007  # los años de trayectoria se calculan desde aquí
COMPANY_SLOGAN = 'Un futuro sembrado hace miles de años'
COMPANY_SLOGAN_EN = 'A future sown thousands of years ago'
# Enlace oficial de Google Maps de la empresa (el mismo del sitio original agrosurlatino.com)
COMPANY_MAPS_URL = (
    'https://www.google.com.pe/maps/place/AGROSUR+LATINO/@-12.0194865,-76.9308707,19z/'
    'data=!3m1!4b1!4m5!3m4!1s0x9105c5444f60ad9f:0xfb1f81ab5ae84c59!8m2!3d-12.0194865!4d-76.9303235'
)
# Teléfono y WhatsApp: se muestran en contacto y pie de página solo si están definidos.
# Definirlos como variables de entorno (ej. COMPANY_PHONE='+51 1 234 5678', COMPANY_WHATSAPP='51987654321').
COMPANY_PHONE = os.environ.get('COMPANY_PHONE', '')
COMPANY_WHATSAPP = os.environ.get('COMPANY_WHATSAPP', '')

# Cotizador
PEN_PER_USD = os.environ.get('PEN_PER_USD', '3.75')  # tipo de cambio: confirmar con el cliente
IGV_RATE = '0.18'
QUOTE_RATE_LIMIT = 5          # envíos por hora y por IP / correo
QUOTE_RATE_WINDOW = 3600

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'landing',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'landing.context.company',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Español en la raíz (/) e inglés bajo /en/ (django.conf.urls.i18n_patterns en config/urls.py)
LANGUAGE_CODE = 'es'
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English'),
]
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
