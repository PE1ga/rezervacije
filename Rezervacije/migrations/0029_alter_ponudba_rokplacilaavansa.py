# Generated by Django 4.1.5 on 2023-05-21 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rezervacije', '0028_vnosgostov_datum_odpovedi_dt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ponudba',
            name='rokPlacilaAvansa',
            field=models.DateTimeField(null=True),
        ),
    ]
