import uuid

from django.db import migrations, models

UNIT_RENAMES = {'CONTENEDOR_40': 'CONTENEDOR_FCL', 'CAJAS': 'SACOS_25KG'}

UNIT_CHOICES = [
    ('CONTENEDOR_FCL', 'Contenedor FCL (~20 TM)'),
    ('PALLET', 'Pallets (1 TM)'),
    ('SACOS_25KG', 'Sacos 25 kg'),
    ('TONELADAS', 'Toneladas Métricas (TM)'),
    ('KILOS', 'Kilos'),
]


def fill_tokens(apps, schema_editor):
    QuoteRequest = apps.get_model('landing', 'QuoteRequest')
    for q in QuoteRequest.objects.all():
        q.public_token = uuid.uuid4()
        q.save(update_fields=['public_token'])


def rename_units(apps, schema_editor):
    QuoteItem = apps.get_model('landing', 'QuoteItem')
    for old, new in UNIT_RENAMES.items():
        QuoteItem.objects.filter(unit=old).update(unit=new)


def revert_units(apps, schema_editor):
    QuoteItem = apps.get_model('landing', 'QuoteItem')
    for old, new in UNIT_RENAMES.items():
        QuoteItem.objects.filter(unit=new).update(unit=old)


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0005_charfield_image_urls'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoterequest',
            name='currency',
            field=models.CharField(choices=[('USD', 'US$'), ('PEN', 'S/')], default='USD', max_length=3, verbose_name='Moneda'),
        ),
        # token: nullable -> relleno por fila -> único
        migrations.AddField(
            model_name='quoterequest',
            name='public_token',
            field=models.UUIDField(null=True, editable=False),
        ),
        migrations.RunPython(fill_tokens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='quoterequest',
            name='public_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Código público (enlace PDF)'),
        ),
        migrations.RunPython(rename_units, revert_units),
        migrations.AlterField(
            model_name='quoteitem',
            name='unit',
            field=models.CharField(choices=UNIT_CHOICES, default='CONTENEDOR_FCL', max_length=40, verbose_name='Unidad de Despacho'),
        ),
        migrations.AlterField(
            model_name='quoteitem',
            name='estimated_subtotal_usd',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True, verbose_name='Subtotal Estimado (moneda de la cotización)'),
        ),
    ]
