# Generated by Django 5.1.5 on 2025-01-23 09:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Пол')),
            ],
            options={
                'verbose_name': 'Пол',
                'verbose_name_plural': 'Пол',
                'db_table': 'gender',
            },
        ),
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=250, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9989999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Телефон'),
        ),
    ]