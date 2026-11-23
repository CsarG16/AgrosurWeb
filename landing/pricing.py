"""Cálculo de precios de cotización. Única fuente de verdad: el navegador nunca fija montos."""
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings

PERU_CLIENT_TYPES = {'NATURAL_DNI', 'NATURAL_RUC', 'JURIDICA_RUC'}

# kg por unidad de despacho
UNIT_KG = {
    'CONTENEDOR_FCL': Decimal('20000'),
    'TONELADAS': Decimal('1000'),
    'PALLET': Decimal('1000'),
    'SACOS_25KG': Decimal('25'),
    'KILOS': Decimal('1'),
}

# cantidad máxima razonable por línea
MAX_QTY = {
    'CONTENEDOR_FCL': Decimal('50'),
    'TONELADAS': Decimal('1000'),
    'PALLET': Decimal('1000'),
    'SACOS_25KG': Decimal('10000'),
    'KILOS': Decimal('100000'),
}

EXPORT_UNITS = ['CONTENEDOR_FCL', 'TONELADAS', 'PALLET', 'SACOS_25KG']
PERU_UNITS = ['SACOS_25KG', 'KILOS']

CENT = Decimal('0.01')


def is_peru_client(client_type):
    return client_type in PERU_CLIENT_TYPES


def currency_for(client_type):
    return 'PEN' if is_peru_client(client_type) else 'USD'


def allowed_units(client_type):
    return PERU_UNITS if is_peru_client(client_type) else EXPORT_UNITS


def unit_price(product, currency):
    """Precio por kg en la moneda de la cotización (S/ incluye IGV)."""
    usd = Decimal(product.ref_price_fob_usd)
    if currency == 'PEN':
        price = usd * Decimal(str(settings.PEN_PER_USD)) * (1 + Decimal(str(settings.IGV_RATE)))
    else:
        price = usd
    return price.quantize(CENT, rounding=ROUND_HALF_UP)


def compute_subtotal(product, qty, unit, currency):
    price = unit_price(product, currency)
    return (Decimal(qty) * UNIT_KG[unit] * price).quantize(CENT, rounding=ROUND_HALF_UP)


def parse_quantity(raw):
    """Devuelve Decimal > 0 o None si no es un número finito válido."""
    try:
        qty = Decimal(str(raw).replace(',', '.').strip())
    except Exception:
        return None
    if not qty.is_finite() or qty <= 0:
        return None
    return qty.quantize(CENT, rounding=ROUND_HALF_UP) or None


def money(amount, currency):
    """Formato fijo (no localizado): US$ 67,687.50 / S/ 1,234.00."""
    symbol = 'S/' if currency == 'PEN' else 'US$'
    return f"{symbol} {Decimal(amount):,.2f}"


# Etiquetas de unidad por idioma: (singular, plural). {} = sin cantidad delante ("× ") para TM/kg.
UNIT_LABELS = {
    'es': {
        'CONTENEDOR_FCL': ('contenedor FCL (~20 TM)', 'contenedores FCL (~20 TM)'),
        'PALLET': ('pallet (1 TM)', 'pallets (1 TM)'),
        'SACOS_25KG': ('saco de 25 kg', 'sacos de 25 kg'),
        'TONELADAS': ('TM', 'TM'),
        'KILOS': ('kg', 'kg'),
    },
    'en': {
        'CONTENEDOR_FCL': ('FCL container (~20 MT)', 'FCL containers (~20 MT)'),
        'PALLET': ('pallet (1 MT)', 'pallets (1 MT)'),
        'SACOS_25KG': ('25 kg bag', '25 kg bags'),
        'TONELADAS': ('MT', 'MT'),
        'KILOS': ('kg', 'kg'),
    },
}
_BARE_UNITS = {'TONELADAS', 'KILOS'}  # "5 TM", "250 kg" (sin "×")


def _plain(qty):
    """Decimal('1.00') -> '1', Decimal('2.50') -> '2.5', Decimal('1000') -> '1000'."""
    return format(Decimal(qty).normalize(), 'f')


def format_quantity(qty, unit, lang='es'):
    """'1 × 25 kg bag', '2 × 25 kg bags', '5 MT'. Misma función para el resumen web y el PDF."""
    labels = UNIT_LABELS.get(lang, UNIT_LABELS['es']).get(unit)
    if not labels:
        return f"{_plain(qty)} {unit}"
    qty = Decimal(qty)
    label = labels[0] if qty == 1 else labels[1]
    sep = ' ' if unit in _BARE_UNITS else ' × '
    return f"{_plain(qty)}{sep}{label}"


def product_name(product, lang='es'):
    return (product.name_en or product.name) if lang == 'en' else product.name
