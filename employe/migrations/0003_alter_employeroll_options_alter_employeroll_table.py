# Generated by Django 5.1.5 on 2025-01-23 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0002_employeroll'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employeroll',
            options={'verbose_name': 'Сотрудники Ролл', 'verbose_name_plural': 'Сотрудники Ролл'},
        ),
        migrations.AlterModelTable(
            name='employeroll',
            table='employe_roll',
        ),
    ]
