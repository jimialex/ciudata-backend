# Generated by Django 4.1.7 on 2023-11-24 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_pendingaction_extra'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Telefono/Celular'),
        ),
    ]
