# Generated by Django 4.1.5 on 2023-02-27 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rezervacije', '0002_sifrantsob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vnosgostov',
            name='Noc_SK',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
