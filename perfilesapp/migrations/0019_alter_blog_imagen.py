# Generated by Django 4.0.5 on 2022-07-21 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfilesapp', '0018_rename_subtitle_blog_subtitulo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='Imagen'),
        ),
    ]