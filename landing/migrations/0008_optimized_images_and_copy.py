import re

from django.db import migrations

# Fotos optimizadas: .png/.jpg -> .webp (products y company). Ver scripts/optimize_images.py
LOCAL_IMAGE = re.compile(r'^(/static/images/(?:products|company)/[a-z\-]+)\.(?:png|jpg|jpeg)$')


def to_webp(value):
    return LOCAL_IMAGE.sub(r'\1.webp', value) if value else value


def forwards(apps, schema_editor):
    for model_name, fields in (
        ('Product', ['image_url']),
        ('ProductCategory', ['image_url']),
        ('HeroSlide', ['image_url', 'secondary_image_url']),
        ('Certification', ['image_url']),
    ):
        Model = apps.get_model('landing', model_name)
        for obj in Model.objects.all():
            changed = []
            for field in fields:
                new = to_webp(getattr(obj, field))
                if new != getattr(obj, field):
                    setattr(obj, field, new)
                    changed.append(field)
            if changed:
                obj.save(update_fields=changed)

    # Logo ÖKO-GARANTIE: la miniatura de 39 px se reemplaza por el original (300 px)
    Certification = apps.get_model('landing', 'Certification')
    Certification.objects.filter(image_url='/static/images/certifications/oko-garantie.jpg').update(
        image_url='/static/images/certifications/oko-garantie.webp'
    )

    Product = apps.get_model('landing', 'Product')
    # Kiwicha tenía la misma foto que Quinua Blanca: ahora usa su propia foto
    Product.objects.filter(name__istartswith='Kiwicha').update(image_url='/static/images/products/kiwicha.webp')
    # En español se escribe "y", no "&"
    Product.objects.filter(name='Pallar Bebé & Pallares').update(name='Pallar Bebé y Pallares')


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0007_product_slug'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
