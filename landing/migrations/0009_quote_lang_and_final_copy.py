from django.db import migrations, models


def forwards(apps, schema_editor):
    CompanyStat = apps.get_model('landing', 'CompanyStat')
    # Los años de trayectoria se calculan en la plantilla desde el año de fundación
    CompanyStat.objects.filter(value='2007').update(label='Año de fundación', label_en='Year founded')
    HeroSlide = apps.get_model('landing', 'HeroSlide')
    HeroSlide.objects.filter(badge='De los productores hacia el mundo').update(
        badge='Un futuro sembrado hace miles de años', badge_en='A future sown thousands of years ago'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0008_optimized_images_and_copy'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoterequest',
            name='lang',
            field=models.CharField(choices=[('es', 'Español'), ('en', 'English')], default='es', max_length=2, verbose_name='Idioma de la cotización (PDF)'),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='incoterm',
            field=models.CharField(
                blank=True,
                choices=[
                    ('FOB', 'FOB (Free On Board - Puerto del Callao)'),
                    ('CIF', 'CIF (Cost, Insurance & Freight)'),
                    ('CFR', 'CFR (Cost & Freight)'),
                    ('EXW', 'EXW (Ex Works - Planta Huachipa, Lima)'),
                ],
                default='FOB',
                help_text='Vacío en cotizaciones para clientes de Perú (RUC 20, RUC 10 y DNI).',
                max_length=10,
                verbose_name='Incoterm Solicitado',
            ),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
