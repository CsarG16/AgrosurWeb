from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0004_certification_image_and_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heroslide',
            name='image_url',
            field=models.CharField(blank=True, help_text='Ruta local (/static/...) o URL externa', max_length=255, null=True, verbose_name='Ruta o URL de Imagen Principal'),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='secondary_image_url',
            field=models.CharField(blank=True, help_text='Ruta local (/static/...) o URL externa para el segundo panel vertical estilo Xpodeka', max_length=255, null=True, verbose_name='Ruta o URL Imagen Secundaria Lateral'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='image_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ruta o URL de Fotografía de Respaldo'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ruta o URL Imagen Respaldo'),
        ),
    ]

