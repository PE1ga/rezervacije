# Generated by Django 4.1.5 on 2023-05-08 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplikacija', '0008_pospravljanjeprihodi_ok1_pospravljanjeprihodi_ok2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pospravljanjeprihodi',
            name='cas_checkin',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='pospravljanjeprihodi',
            name='st_noci',
            field=models.IntegerField(null=True),
        ),
    ]
