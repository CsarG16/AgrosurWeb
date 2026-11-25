from django.db import migrations


def forwards(apps, schema_editor):
    # Nueva foto del banner: agricultor andino con chaquitaclla en un campo de quinua
    HeroSlide = apps.get_model('landing', 'HeroSlide')
    HeroSlide.objects.filter(image_url='/static/images/company/campo-atardecer.webp').update(
        image_url='/static/images/company/hero-quinua.webp'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0012_official_cert_logos'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
