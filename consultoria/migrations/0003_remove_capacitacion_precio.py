# Generated by Django 5.1.2 on 2024-12-11 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultoria', '0002_capacitacion_servicio_delete_servicioconsultoria_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='capacitacion',
            name='precio',
        ),
    ]
