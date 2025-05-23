# Generated by Django 3.1.12 on 2025-05-06 18:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo electrónico')),
                ('can_receive_emails', models.BooleanField(default=False)),
                ('password', models.CharField(max_length=128, verbose_name='Contraseña')),
                ('foto_perfil', models.CharField(blank=True, max_length=255, null=True, verbose_name='Foto de perfil')),
                ('instagram_username', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('role', models.CharField(choices=[('admin', 'Administrador'), ('user', 'Usuario normal')], default='user', max_length=10)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha de la cita')),
                ('hora', models.TimeField(verbose_name='Hora de la cita')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada'), ('completada', 'Completada'), ('cancelada', 'Cancelada')], default='pendiente', max_length=50)),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción adicional')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Design',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField()),
                ('titulo', models.CharField(max_length=150)),
                ('descripcion', models.CharField(max_length=500)),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('alto', models.IntegerField()),
                ('ancho', models.IntegerField()),
                ('duracion', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_emision', models.DateField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('cita', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='factura', to='api.cita')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facturas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
