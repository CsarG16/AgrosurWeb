from django.db import migrations, models
from django.utils.text import slugify


def fill_slugs(apps, schema_editor):
    Product = apps.get_model('landing', 'Product')
    used = set()
    for product in Product.objects.order_by('id'):
        base = slugify(product.name)[:130] or 'producto'
        slug, n = base, 2
        while slug in used:
            slug = f"{base}-{n}"
            n += 1
        used.add(slug)
        product.slug = slug
        product.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0006_quote_token_currency_units'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=140, null=True, verbose_name='Identificador (slug)'),
        ),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(
                blank=True,
                help_text='Se genera solo desde el nombre. Se usa en enlaces como /cotizador/?producto=habas-secas',
                max_length=140,
                unique=True,
                verbose_name='Identificador (slug)',
            ),
        ),
    ]
