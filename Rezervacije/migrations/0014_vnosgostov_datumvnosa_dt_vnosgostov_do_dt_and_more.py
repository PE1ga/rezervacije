# Generated by Django 4.1.5 on 2023-03-27 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rezervacije', '0013_ponudba_do_dt_ponudba_od_dt'),
    ]

    operations = [
        migrations.AddField(
            model_name='vnosgostov',
            name='datumVnosa_dt',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='vnosgostov',
            name='do_dt',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='vnosgostov',
            name='od_dt',
            field=models.DateTimeField(null=True),
        ),
    ]
