# Generated by Django 5.2.3 on 2025-06-22 18:04

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habito', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckDiario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(default=django.utils.timezone.now)),
                ('feito', models.BooleanField(default=False)),
                ('habito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='habito.habito')),
            ],
        ),
    ]
