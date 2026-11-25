from django.db import migrations


def forwards(apps, schema_editor):
    Certification = apps.get_model('landing', 'Certification')
    # Logos oficiales descargados de la fuente de cada ente (USDA AMS y Comisión Europea)
    Certification.objects.filter(image_url='/static/images/certifications/usda-organic.png').update(
        image_url='/static/images/certifications/usda-organic.webp'
    )
    Certification.objects.filter(image_url='/static/images/certifications/eu-organic.jpeg').update(
        image_url='/static/images/certifications/eu-organic.webp'
    )
    # Logos sin fondo blanco (transparentes): solo el logo, sin recuadro
    for old, new in [
        ('jas.jpg', 'jas-logo.webp'),
        ('oko-garantie.webp', 'oko-garantie-logo.webp'),
        ('brcgs.webp', 'brcgs-logo.webp'),
        ('fda.jpg', 'fda-logo.webp'),
    ]:
        Certification.objects.filter(image_url=f'/static/images/certifications/{old}').update(
            image_url=f'/static/images/certifications/{new}'
        )


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0011_quoteitem_product_protect'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
