# Generated by Django 4.1.5 on 2023-05-21 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rezervacije', '0030_alter_vnosgostov_rokplacilaavansa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vnosgostov',
            name='RokPlacilaAvansa',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
