# Generated by Django 4.0.5 on 2022-07-09 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfilesapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nosotros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Profesores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreprofesor', models.CharField(max_length=30, verbose_name='Nombre Profesor')),
                ('apellidoprofesor', models.CharField(max_length=30, verbose_name='Apellido Profesor')),
                ('edadprofesor', models.SmallIntegerField(verbose_name='Edad')),
                ('fechanacimientoprofesor', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('emailprofesor', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('sexoprofesor', models.PositiveSmallIntegerField(choices=[(1, 'Femenino'), (2, 'Masculino')], verbose_name='Sexo')),
                ('especialidad', models.PositiveSmallIntegerField(choices=[(1, 'Remo'), (2, 'Vela'), (3, 'Kayak')], verbose_name='Especialidad')),
            ],
        ),
        migrations.CreateModel(
            name='Socios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre Socio')),
                ('apellido', models.CharField(max_length=30, verbose_name='Apellido Socio')),
                ('edad', models.SmallIntegerField(verbose_name='Edad')),
                ('fechanacimiento', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('sexo', models.PositiveSmallIntegerField(choices=[(1, 'Femenino'), (2, 'Masculino')], verbose_name='Sexo')),
            ],
        ),
        migrations.CreateModel(
            name='TiendaObjetos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto', models.CharField(max_length=30, verbose_name='Producto')),
                ('descripcion', models.CharField(max_length=150, verbose_name='Descripcion Producto')),
                ('precio', models.FloatField(verbose_name='Precio $')),
            ],
        ),
        migrations.AlterField(
            model_name='tiendaactividades',
            name='actividad',
            field=models.SmallIntegerField(choices=[(1, 'Remo'), (2, 'Vela'), (3, 'Kayak')], verbose_name='Actividad'),
        ),
        migrations.AlterField(
            model_name='tiendaactividades',
            name='turno',
            field=models.PositiveSmallIntegerField(choices=[(1, 'mañana'), (2, 'tarde'), (3, 'noche')], verbose_name='Turno'),
        ),
    ]
