# Generated by Django 4.1.5 on 2023-04-08 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rezervacije', '0019_remove_bar_cenik_bruto_suma_z_ddv_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar_narocila',
            name='kolicina',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
