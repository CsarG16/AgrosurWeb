from django.db import migrations, models

# Catálogo actual: solo quinuas (superalimentos) y frejoles. El resto se oculta (no se borra).
HIDDEN_PRODUCTS = [
    'chia-en-grano', 'kiwicha-amaranto-en-grano', 'pallar-bebe-pallares',
    'zarandaja', 'habas-secas', 'maiz-gigante-del-cusco',
]


def forwards(apps, schema_editor):
    Product = apps.get_model('landing', 'Product')
    ProductCategory = apps.get_model('landing', 'ProductCategory')
    Product.objects.filter(slug__in=HIDDEN_PRODUCTS).update(is_active=False)
    Product.objects.filter(slug__startswith='quinua-').update(is_superfood=True)
    ProductCategory.objects.filter(slug='granos-andinos').update(
        name='Quinuas – Superalimentos', name_en='Quinoa – Superfoods'
    )
    # sin productos activos: se oculta del menú y de los filtros
    ProductCategory.objects.filter(slug='maices-cultivos').update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0013_hero_quinua_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_superfood',
            field=models.BooleanField(default=False, help_text='Muestra la etiqueta SUPERALIMENTO en la tarjeta del producto.', verbose_name='Superalimento'),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
