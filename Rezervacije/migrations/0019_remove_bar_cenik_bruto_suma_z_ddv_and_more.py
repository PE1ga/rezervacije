# Generated by Django 4.1.5 on 2023-04-07 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Rezervacije', '0018_bar_narocila'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bar_cenik',
            name='bruto_suma_z_ddv',
        ),
        migrations.RemoveField(
            model_name='bar_cenik',
            name='bruto_z_ddv',
        ),
        migrations.RemoveField(
            model_name='bar_cenik',
            name='kolicina',
        ),
    ]
