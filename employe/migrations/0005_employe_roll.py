# Generated by Django 5.1.5 on 2025-01-23 17:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0004_employeroll_owner_alter_employeroll_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employe',
            name='roll',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employe.employeroll', verbose_name='Ролл'),
        ),
    ]
