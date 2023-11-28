# Generated by Django 4.1.7 on 2023-11-28 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciudata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='plate',
            field=models.CharField(max_length=8, unique=True, verbose_name='Placa'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='slug',
            field=models.SlugField(default='A7C00B8AE8', unique=True, verbose_name='Slug'),
        ),
    ]